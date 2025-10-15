import unittest
from unittest.mock import MagicMock, patch
from tmux_predefined_layout import (
    TmuxSessionManager,
    _parse_json_to_config,
    SessionConfig,
    WindowConfig,
    PaneConfig,
)


class TestTmuxSessionManager(unittest.TestCase):
    def setUp(self):
        # Patch libtmux.Server so no real tmux connection is made
        patcher = patch("tmux_session.libtmux.Server")
        self.mock_server_class = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_server = MagicMock()
        self.mock_server_class.return_value = self.mock_server

        # Mock session and window objects
        self.mock_session = MagicMock()
        self.mock_server.list_sessions.return_value = [self.mock_session]
        self.mock_session.name = "test_session"
        self.mock_session.windows = []

        self.manager = TmuxSessionManager("test_session")
        self.manager.server = self.mock_server  # Inject mock server

    def test_get_session_exists(self):
        # Should find existing session
        self.mock_server.list_sessions.return_value = [self.mock_session]
        session = self.manager.get_session()
        self.assertEqual(session, self.mock_session)

    def test_get_session_not_exists(self):
        # No session returns None
        self.mock_server.list_sessions.return_value = []
        session = self.manager.get_session()
        self.assertIsNone(session)

    def test_create_session_already_exists(self):
        self.mock_server.list_sessions.return_value = [self.mock_session]
        with self.assertLogs("tmux_manager", level="INFO") as cm:
            self.manager.create_session()
            self.assertIn("already exists", "\n".join(cm.output))

    def test_create_session_new(self):
        self.mock_server.list_sessions.return_value = []
        self.mock_server.new_session.return_value = self.mock_session
        self.manager.create_session()
        self.mock_server.new_session.assert_called_once_with(
            session_name="test_session", attach=False
        )

    def test_kill_session_exists(self):
        self.mock_server.list_sessions.return_value = [self.mock_session]
        self.manager.session = self.mock_session
        self.manager.kill_session()
        self.mock_session.kill_session.assert_called_once()

    def test_kill_session_not_exists(self):
        self.mock_server.list_sessions.return_value = []
        with self.assertLogs("tmux_manager", level="WARNING") as cm:
            self.manager.kill_session()
            self.assertIn("does not exist", "\n".join(cm.output))

    def test_parse_json_to_config_valid(self):
        json_data = {
            "name": "my_session",
            "windows": [
                {
                    "name": "win1",
                    "layout": "tiled",
                    "panes": [{"name": "pane1", "command": "echo hi"}],
                }
            ],
            "options": {"mouse": True},
            "pre_commands": ["echo pre"],
            "post_commands": ["echo post"],
        }
        config = _parse_json_to_config(json_data)
        self.assertIsInstance(config, SessionConfig)
        self.assertEqual(config.name, "my_session")
        self.assertEqual(len(config.windows), 1)
        self.assertTrue(config.options["mouse"])
        self.assertEqual(config.pre_commands, ["echo pre"])
        self.assertEqual(config.post_commands, ["echo post"])

    def test_parse_json_to_config_missing_name(self):
        json_data = {}
        with self.assertRaises(ValueError):
            _parse_json_to_config(json_data)

    # More tests can be added for _apply_session_options, _configure_pane, etc.
    # Those would require mocking tmux commands or the panes/windows more deeply.


if __name__ == "__main__":
    unittest.main()
