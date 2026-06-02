"""Tests for ai_commit_writer."""
import pytest
from unittest.mock import patch, MagicMock
from ai_commit_writer import query_ollama, get_git_diff

class TestGetGitDiff:
    def test_returns_string(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = "diff --git a/file.py b/file.py"
            mock_run.return_value.returncode = 0
            result = get_git_diff(staged=True)
            assert "diff --git" in result

    def test_empty_diff(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = ""
            mock_run.return_value.returncode = 0
            result = get_git_diff(staged=True)
            assert result == ""

    def test_no_changes_message(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = ""
            mock_run.return_value.returncode = 0
            result = get_git_diff(staged=False)
            assert isinstance(result, str)

class TestQueryOllama:
    def test_generates_commit_message(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"response": "feat: add new feature"}
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_resp
            result = query_ollama("diff content", "test-model")
            assert "feat:" in result

    def test_handles_api_error(self):
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = Exception("API error")
            result = query_ollama("diff", "test-model")
            assert "Error" in result
