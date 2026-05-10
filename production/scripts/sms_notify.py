"""SMS notifications for render lifecycle events.

Integration contract for issue #1's render loop
------------------------------------------------
Import this module at the top of render_scene.py (or the render orchestrator):

    import production.scripts.sms_notify as sms

Then call at lifecycle boundaries:

    sms.notify("render_queue_start", scene_count=14)
    sms.notify("scene_complete",     scene_name="Act.1-Scene.5-Beach", elapsed_s=382)
    sms.notify("scene_aborted",      scene_name="Act.2-Scene.3-Alley", frame=48, consecutive_fails=3)
    sms.notify("structural_failure", scene_name="Act.3-Scene.1-Roof",
                                     check_name="frame_count_mismatch",
                                     detail="got 96, expected 240")
    sms.notify("blender_crash",      scene_name="Act.3-Scene.1-Roof", exit_code=1)
    sms.notify("render_queue_complete", total=14, aborted=2, elapsed_s=7421)

All calls are safe to make whether or not SMS is enabled. When disabled (the
default) every call is a no-op. Failure to send never raises; the render
continues regardless.

Env vars
--------
NOTIFY_SMS_ENABLED        Set to "1" to activate. Absent or "0" = fully disabled.
NOTIFY_SMS_TO             Recipient E.164 phone number, e.g. +15555550100
TWILIO_ACCOUNT_SID        Twilio account SID
TWILIO_AUTH_TOKEN         Twilio auth token
TWILIO_FROM               Twilio sender number, e.g. +15550000001
NOTIFY_SMS_PER_SCENE      Set to "0" to suppress per-scene complete messages (default: "1")
NOTIFY_SMS_QUIET_START    HH:MM in 24h UTC, e.g. "22:00" (default: no quiet hours)
NOTIFY_SMS_QUIET_END      HH:MM in 24h UTC, e.g. "07:00" (default: no quiet hours)
NOTIFY_SMS_DRY_RUN        Set to "1" to log the message that would be sent without
                          making any Twilio API call. Useful for first-run validation.
NOTIFY_SMS_TEST_RECIPIENT Used by --send-test CLI; overrides NOTIFY_SMS_TO for one message.

Quiet-hours behaviour
---------------------
During quiet hours, non-critical messages are DROPPED (not queued for later).
A line is logged explaining the suppression.
Critical events (scene_aborted, structural_failure, blender_crash) bypass quiet
hours and are always sent when SMS is enabled.

Twilio cost note
----------------
~$0.01/SMS for US numbers. A 14-scene render with per-scene messages enabled is
approximately 16 SMS ($0.16). Disable NOTIFY_SMS_PER_SCENE to reduce to 2 SMS.
"""

import base64
import json
import logging
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Module-level logger — callers see "sms_notify" in log output
# ---------------------------------------------------------------------------
log = logging.getLogger("sms_notify")
if not log.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s %(message)s"))
    log.addHandler(_handler)
    log.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _is_enabled() -> bool:
    return _env("NOTIFY_SMS_ENABLED") == "1"


def _is_dry_run() -> bool:
    return _env("NOTIFY_SMS_DRY_RUN") == "1"


def _per_scene_enabled() -> bool:
    return _env("NOTIFY_SMS_PER_SCENE", "1") != "0"


def _utc_now_iso() -> str:
    """Return compact UTC ISO timestamp, e.g. 2026-05-10T02:31:00Z"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _in_quiet_hours() -> bool:
    """Return True if current UTC time falls inside the configured quiet window."""
    quiet_start = _env("NOTIFY_SMS_QUIET_START")
    quiet_end = _env("NOTIFY_SMS_QUIET_END")
    if not quiet_start or not quiet_end:
        return False

    try:
        now_utc = datetime.now(timezone.utc)
        now_minutes = now_utc.hour * 60 + now_utc.minute

        def _parse(t: str) -> int:
            h, m = t.split(":")
            return int(h) * 60 + int(m)

        start = _parse(quiet_start)
        end = _parse(quiet_end)

        # Quiet window may wrap midnight (e.g., 22:00 to 07:00)
        if start <= end:
            return start <= now_minutes < end
        else:
            # Wraps midnight: active when >= start OR < end
            return now_minutes >= start or now_minutes < end
    except Exception as exc:
        log.warning("sms_notify: could not parse quiet hours (%s); ignoring", exc)
        return False


def _send_sms(body: str, recipient: str | None = None) -> bool:
    """
    Send a single SMS via Twilio REST API using urllib.request.
    Returns True on success, False on any failure (never raises).
    """
    to = recipient or _env("NOTIFY_SMS_TO")
    account_sid = _env("TWILIO_ACCOUNT_SID")
    auth_token = _env("TWILIO_AUTH_TOKEN")
    from_number = _env("TWILIO_FROM")

    if not all([to, account_sid, auth_token, from_number]):
        log.error(
            "sms_notify: missing Twilio config — need NOTIFY_SMS_TO, "
            "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM"
        )
        return False

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    payload = urllib.parse.urlencode({"To": to, "From": from_number, "Body": body}).encode()
    credentials = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            if 200 <= status < 300:
                log.info("sms_notify: SMS sent (HTTP %s)", status)
                return True
            # Unexpected 2xx — still succeeded
            log.warning("sms_notify: unexpected HTTP status %s sending SMS", status)
            return True
    except urllib.error.HTTPError as exc:
        try:
            err_body = exc.read().decode(errors="replace")
            detail = json.loads(err_body).get("message", err_body[:200])
        except Exception:
            detail = str(exc)
        log.error("sms_notify: Twilio API error %s — %s", exc.code, detail)
        return False
    except urllib.error.URLError as exc:
        log.error("sms_notify: network error sending SMS — %s", exc.reason)
        return False
    except Exception as exc:
        log.error("sms_notify: unexpected error sending SMS — %s", exc)
        return False


def _dispatch(body: str, critical: bool = False, recipient: str | None = None) -> None:
    """
    Central dispatch: apply quiet-hours logic, dry-run bypass, then send.
    Never raises.
    """
    if not critical and _in_quiet_hours():
        log.info(
            "sms_notify: message suppressed (quiet hours active, non-critical): %s", body
        )
        return

    if _is_dry_run():
        log.info("sms_notify: [DRY RUN] Would send SMS: %s", body)
        return

    _send_sms(body, recipient=recipient)


# ---------------------------------------------------------------------------
# Event handlers — one per lifecycle event
# ---------------------------------------------------------------------------

def _handle_render_queue_start(scene_count: int) -> None:
    ts = _utc_now_iso()
    body = f"[START] Catalysis render started, {scene_count} scenes [{ts}]"
    _dispatch(body, critical=False)


def _handle_scene_complete(scene_name: str, elapsed_s: float) -> None:
    if not _per_scene_enabled():
        log.debug("sms_notify: per-scene SMS disabled; skipping scene_complete for %s", scene_name)
        return
    minutes = int(elapsed_s) // 60
    seconds = int(elapsed_s) % 60
    ts = _utc_now_iso()
    body = f"[OK] {scene_name}: done in {minutes}m {seconds}s [{ts}]"
    _dispatch(body, critical=False)


def _handle_scene_aborted(scene_name: str, frame: int, consecutive_fails: int) -> None:
    ts = _utc_now_iso()
    body = (
        f"[ABORT] {scene_name}: {consecutive_fails} vision fails at frame {frame} [{ts}]"
    )
    _dispatch(body, critical=True)


def _handle_structural_failure(scene_name: str, check_name: str, detail: str) -> None:
    ts = _utc_now_iso()
    body = f"[FAIL] {scene_name}: {check_name} — {detail} [{ts}]"
    _dispatch(body, critical=True)


def _handle_blender_crash(scene_name: str, exit_code: int) -> None:
    ts = _utc_now_iso()
    body = f"[CRASH] {scene_name}: Blender exited with code {exit_code} [{ts}]"
    _dispatch(body, critical=True)


def _handle_render_queue_complete(total: int, aborted: int, elapsed_s: float) -> None:
    minutes = int(elapsed_s) // 60
    ts = _utc_now_iso()
    body = (
        f"[DONE] All {total} scenes, {aborted} aborted, {minutes} min total [{ts}]"
    )
    _dispatch(body, critical=False)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_HANDLERS = {
    "render_queue_start":    _handle_render_queue_start,
    "scene_complete":        _handle_scene_complete,
    "scene_aborted":         _handle_scene_aborted,
    "structural_failure":    _handle_structural_failure,
    "blender_crash":         _handle_blender_crash,
    "render_queue_complete": _handle_render_queue_complete,
}


def notify(event_name: str, **kwargs) -> None:
    """Dispatch a lifecycle notification.

    Safe to call at any time. If SMS is not enabled (NOTIFY_SMS_ENABLED != "1"),
    this is a cheap no-op. Never raises; SMS failures are logged and swallowed
    so the render loop is never interrupted by a notification failure.

    Args:
        event_name: One of: render_queue_start, scene_complete, scene_aborted,
                    structural_failure, blender_crash, render_queue_complete.
        **kwargs:   Event-specific keyword arguments (see integration contract
                    in module docstring).
    """
    if not _is_enabled() and not _is_dry_run():
        return

    handler = _HANDLERS.get(event_name)
    if handler is None:
        log.warning("sms_notify: unknown event '%s'; ignored", event_name)
        return

    try:
        handler(**kwargs)
    except TypeError as exc:
        log.error("sms_notify: bad kwargs for event '%s' — %s", event_name, exc)
    except Exception as exc:
        log.error("sms_notify: unhandled error in handler for '%s' — %s", event_name, exc)


# ---------------------------------------------------------------------------
# CLI entrypoints (not for production use; for first-run validation only)
# ---------------------------------------------------------------------------

def _run_dry_run_test() -> None:
    """Print formatted messages for every event type without making any HTTP call."""
    print("sms_notify --test: exercising all 6 event handlers in dry-run mode\n")
    os.environ["NOTIFY_SMS_DRY_RUN"] = "1"
    os.environ["NOTIFY_SMS_ENABLED"] = "1"

    test_cases = [
        ("render_queue_start",    {"scene_count": 14}),
        ("scene_complete",        {"scene_name": "Act.1-Scene.5-Beach", "elapsed_s": 382}),
        ("scene_aborted",         {"scene_name": "Act.2-Scene.3-Alley", "frame": 48,
                                   "consecutive_fails": 3}),
        ("structural_failure",    {"scene_name": "Act.3-Scene.1-Roof",
                                   "check_name": "frame_count_mismatch",
                                   "detail": "got 96, expected 240"}),
        ("blender_crash",         {"scene_name": "Act.3-Scene.2-Crane", "exit_code": 1}),
        ("render_queue_complete", {"total": 14, "aborted": 2, "elapsed_s": 7421}),
    ]

    for event, kwargs in test_cases:
        print(f"--- Event: {event} ---")
        notify(event, **kwargs)
        print()

    # Also test quiet-hours suppression of a non-critical event
    print("--- Quiet-hours suppression test (non-critical, always-quiet window) ---")
    os.environ["NOTIFY_SMS_QUIET_START"] = "00:00"
    os.environ["NOTIFY_SMS_QUIET_END"]   = "23:59"
    notify("scene_complete", scene_name="Act.1-Scene.1-Apartment", elapsed_s=120)
    print()

    # Critical event should bypass quiet hours
    print("--- Quiet-hours bypass test (critical event, always-quiet window) ---")
    notify("blender_crash", scene_name="Act.1-Scene.2-Kitchen", exit_code=139)
    print()

    print("All event handlers exercised. Review log output above for message bodies.")


def _run_send_test() -> None:
    """Send a single live SMS to NOTIFY_SMS_TEST_RECIPIENT to validate Twilio credentials."""
    recipient = _env("NOTIFY_SMS_TEST_RECIPIENT")
    if not recipient:
        print(
            "Error: set NOTIFY_SMS_TEST_RECIPIENT=+15555555555 before running --send-test",
            file=sys.stderr,
        )
        sys.exit(1)

    os.environ["NOTIFY_SMS_ENABLED"] = "1"
    ts = _utc_now_iso()
    body = f"[TEST] sms_notify credential check — if you see this, Twilio is configured correctly [{ts}]"

    print(f"Sending test SMS to {recipient} ...")
    success = _send_sms(body, recipient=recipient)
    if success:
        print("SMS sent successfully.")
    else:
        print("SMS failed — check log output above for details.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if "--test" in sys.argv:
        _run_dry_run_test()
    elif "--send-test" in sys.argv:
        _run_send_test()
    else:
        print(
            "Usage:\n"
            "  python -m production.scripts.sms_notify --test\n"
            "      Dry-run: print formatted messages for all 6 event types\n\n"
            "  NOTIFY_SMS_TEST_RECIPIENT=+15555555555 "
            "python -m production.scripts.sms_notify --send-test\n"
            "      Send one live SMS to validate Twilio credentials",
            file=sys.stderr,
        )
        sys.exit(1)
