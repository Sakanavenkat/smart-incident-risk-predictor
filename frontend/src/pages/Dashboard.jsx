import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Card,
  CardContent
} from '@mui/material';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DescriptionIcon from '@mui/icons-material/Description';
import ErrorIcon from '@mui/icons-material/Error';
import axios from 'axios';

const API_BASE = '/api';

// Colors for charts
const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1'];
const PRIORITY_COLORS = {
  P1: '#ff4444',
  P2: '#ff9800',
  P3: '#ffc107',
  P4: '#4caf50',
  P5: '#2196f3'
};

// Stat card component
const StatCard = ({ title, value, subtitle, icon: Icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box>
          <Typography color="textSecondary" gutterBottom>
            {title}
          </Typography>
          <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
            {value}
          </Typography>
          {subtitle && (
            <Typography variant="caption" color="textSecondary">
              {subtitle}
            </Typography>
          )}
        </Box>
        {Icon && (
          <Icon sx={{ fontSize: 40, color: color || '#8884d8' }} />
        )}
      </Box>
    </CardContent>
  </Card>
);

// Main dashboard component
export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Get token from localStorage
  const getToken = () => localStorage.getItem('token');

  // Fetch dashboard data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const token = getToken();
        const response = await axios.get(`${API_BASE}/dashboard/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setData(response.data);
        setError(null);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError(err.response?.data?.detail || 'Failed to load dashboard data');
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading dashboard...</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!data) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="warning">No data available</Alert>
      </Container>
    );
  }

  const { summary, priority_distribution, status_distribution, region_distribution, 
          category_performance, assignment_group_workload, sla_trend, oldest_tickets } = data;

  // Prepare chart data
  const priorityChartData = Object.entries(priority_distribution).map(([priority, count]) => ({
    name: priority,
    value: count
  }));

  const statusChartData = Object.entries(status_distribution).map(([status, count]) => ({
    name: status,
    value: count
  }));

  const regionChartData = Object.entries(region_distribution).map(([region, count]) => ({
    name: region,
    value: count
  }));

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
          Incident Dashboard
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Real-time monitoring and analytics
        </Typography>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Total Tickets"
            value={summary.total_tickets}
            icon={DescriptionIcon}
            color="#2196f3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Open Tickets"
            value={summary.open_tickets}
            subtitle={`${summary.in_progress_tickets} in progress`}
            icon={ErrorIcon}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="High Risk (P1-P2)"
            value={summary.high_risk_tickets}
            icon={WarningIcon}
            color="#f44336"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Closed Tickets"
            value={summary.closed_tickets}
            icon={CheckCircleIcon}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Average SLA"
            value={`${summary.average_sla_percentage}%`}
            icon={null}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Oldest Open"
            value={oldest_tickets.length > 0 ? `${oldest_tickets[0].open_days} days` : 'N/A'}
            subtitle={oldest_tickets.length > 0 ? oldest_tickets[0].ticket_id : ''}
            icon={null}
          />
        </Grid>
      </Grid>

      {/* Charts Row 1 */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {/* Priority Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              Priority Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={priorityChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8">
                  {priorityChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={PRIORITY_COLORS[entry.name]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Status Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              Status Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={statusChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {statusChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Charts Row 2 */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {/* SLA Trend */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              SLA Trend (Last 7 Days)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={sla_trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="average_sla"
                  stroke="#8884d8"
                  strokeWidth={2}
                  name="Average SLA %"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Region Distribution */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              By Region
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={regionChartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="value" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Charts Row 3 */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {/* Category Performance */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              Category Performance
            </Typography>
            <Box sx={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid #ddd' }}>
                    <th style={{ textAlign: 'left', padding: '8px' }}>Category</th>
                    <th style={{ textAlign: 'center', padding: '8px' }}>Total</th>
                    <th style={{ textAlign: 'center', padding: '8px' }}>Closed</th>
                    <th style={{ textAlign: 'right', padding: '8px' }}>Rate</th>
                    <th style={{ textAlign: 'right', padding: '8px' }}>Avg SLA</th>
                  </tr>
                </thead>
                <tbody>
                  {category_performance.map((cat) => (
                    <tr key={cat.category} style={{ borderBottom: '1px solid #eee' }}>
                      <td style={{ padding: '8px' }}>{cat.category}</td>
                      <td style={{ textAlign: 'center', padding: '8px' }}>{cat.total}</td>
                      <td style={{ textAlign: 'center', padding: '8px' }}>{cat.closed}</td>
                      <td style={{ textAlign: 'right', padding: '8px', color: '#2196f3', fontWeight: 'bold' }}>
                        {cat.closure_rate}%
                      </td>
                      <td style={{ textAlign: 'right', padding: '8px' }}>{cat.average_sla}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Box>
          </Paper>
        </Grid>

        {/* Assignment Group Workload */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
              Assignment Group Workload
            </Typography>
            <Box sx={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid #ddd' }}>
                    <th style={{ textAlign: 'left', padding: '8px' }}>Group</th>
                    <th style={{ textAlign: 'center', padding: '8px' }}>Total</th>
                    <th style={{ textAlign: 'center', padding: '8px' }}>Open</th>
                    <th style={{ textAlign: 'right', padding: '8px' }}>Avg SLA</th>
                  </tr>
                </thead>
                <tbody>
                  {assignment_group_workload.map((group) => (
                    <tr key={group.assignment_group} style={{ borderBottom: '1px solid #eee' }}>
                      <td style={{ padding: '8px' }}>{group.assignment_group}</td>
                      <td style={{ textAlign: 'center', padding: '8px' }}>{group.total_tickets}</td>
                      <td style={{ textAlign: 'center', padding: '8px', color: group.open_tickets > 5 ? '#f44336' : '#666' }}>
                        {group.open_tickets}
                      </td>
                      <td style={{ textAlign: 'right', padding: '8px' }}>{group.average_sla}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Oldest Tickets */}
      {oldest_tickets.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
            Oldest Open Tickets
          </Typography>
          <Box sx={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #ddd' }}>
                  <th style={{ textAlign: 'left', padding: '8px' }}>Ticket ID</th>
                  <th style={{ textAlign: 'center', padding: '8px' }}>Priority</th>
                  <th style={{ textAlign: 'center', padding: '8px' }}>Category</th>
                  <th style={{ textAlign: 'center', padding: '8px' }}>Open Days</th>
                  <th style={{ textAlign: 'right', padding: '8px' }}>SLA %</th>
                  <th style={{ textAlign: 'center', padding: '8px' }}>Assigned To</th>
                </tr>
              </thead>
              <tbody>
                {oldest_tickets.map((ticket) => (
                  <tr key={ticket.id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '8px', fontWeight: 'bold' }}>{ticket.ticket_id}</td>
                    <td style={{ textAlign: 'center', padding: '8px' }}>
                      <span style={{ 
                        background: PRIORITY_COLORS[ticket.priority], 
                        color: 'white', 
                        padding: '4px 8px', 
                        borderRadius: '4px',
                        fontSize: '0.85em'
                      }}>
                        {ticket.priority}
                      </span>
                    </td>
                    <td style={{ textAlign: 'center', padding: '8px' }}>{ticket.category}</td>
                    <td style={{ textAlign: 'center', padding: '8px', color: ticket.open_days > 30 ? '#f44336' : '#666' }}>
                      {ticket.open_days}
                    </td>
                    <td style={{ textAlign: 'right', padding: '8px' }}>{ticket.sla_percentage}%</td>
                    <td style={{ textAlign: 'center', padding: '8px', fontSize: '0.9em' }}>
                      {ticket.assignment_group}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Box>
        </Paper>
      )}
    </Container>
  );
}
