"""
Module for testing the MCP server creation and functionality.

This module contains unit tests for the server setup of the HK Law MCP Server.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_law_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """Test class for verifying MCP server creation and tool functionality."""
    @patch("hkopenai.hk_law_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_law_mcp_server.server.foreign_domestic_helpers")
    def test_create_mcp_server(self, mock_foreign_domestic_helpers, mock_fastmcp):
        """Test the creation and configuration of the MCP server with mocked dependencies."""
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 1)

        # Get all decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_server.tool.return_value.call_args_list
        }
        self.assertEqual(len(decorated_funcs), 1)

        # Call each decorated function and verify that the correct underlying function is called

        decorated_funcs["get_fdh_statistics"](year=2023)
        mock_foreign_domestic_helpers.get_fdh_statistics.assert_called_once_with(2023)


if __name__ == "__main__":
    unittest.main()
