import unittest
from unittest.mock import patch, mock_open, MagicMock

from statistics_handler import StatisticsManager

class TestStatisticsManager(unittest.TestCase):

    def setUp(self):
        self.instances = [MagicMock(id='i-12345', public_dns_name='temp_dns')]
        self.key_path = '/path/to/key'
        self.log_type = 'json'
        self.manager = StatisticsManager(self.log_type, self.instances, self.key_path)

    @patch('src.statistics_handler.SSHManager')
    @patch('builtins.open', new_callable=mock_open, read_data='{"create_time": "time1", "copy_time": "time2", "delete_time": "time3"}')
    def test_gather_statistics(self, mock_open, MockSSHManager):
        mock_ssh_instance = MockSSHManager.return_value
        mock_ssh_instance.get_file.return_value = None
        
        stats = self.manager.gather_statistics(self.instances[0])
        
        mock_ssh_instance.get_file.assert_called_once_with('/home/ubuntu/stats.json', 'stats_i-12345.json')
        mock_open.assert_called_once_with('stats_i-12345.json', 'r')
        self.assertEqual(stats, {"create_time": "time1", "copy_time": "time2", "delete_time": "time3"})

    @patch.object(StatisticsManager, 'gather_statistics')
    def test_gather_all_statistics(self, mock_gather_statistics):
        mock_gather_statistics.return_value = {"create_time": "time1", "copy_time": "time2", "delete_time": "time3"}
        self.manager.gather_all_statistics()
        mock_gather_statistics.assert_called_once_with(self.instances[0])
        self.assertIn('i-12345', self.manager.all_stats)
        self.assertEqual(self.manager.all_stats['i-12345'], {"create_time": "time1", "copy_time": "time2", "delete_time": "time3"})

 
if __name__ == '__main__':
    unittest.main()
