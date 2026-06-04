# Dashboard & Frontend Guide

## Overview

The Smart Incident Risk Predictor includes a React-based dashboard for real-time monitoring and analytics of incident tickets. This guide covers setup, architecture, and features.

---

## 📋 Prerequisites

### Backend Running
The backend API must be running on `http://localhost:8000`

```bash
# Start backend
run.bat  # Windows
bash run.sh  # Unix/macOS
```

### Node.js Installed
- Node.js 16+ 
- npm 8+ 

Check versions:
```bash
node --version
npm --version
```

---

## 🚀 Installation & Setup

### Step 1: Install Frontend Dependencies

**Windows:**
```bash
frontend-install.bat
```

**macOS/Linux:**
```bash
bash frontend-install.sh
```

This will:
1. Navigate to `frontend/` directory
2. Run `npm install` to install all dependencies
3. Create `node_modules/` directory

### Step 2: Start Frontend Development Server

**Windows:**
```bash
frontend-run.bat
```

**macOS/Linux:**
```bash
bash frontend-run.sh
```

The dashboard will be available at: **http://localhost:3000**

---

## 🎯 Using the Dashboard

### Login

Default credentials:
- Email: `admin@example.com`
- Password: `Admin@123456`

After login, you'll see the main dashboard.

### Dashboard Sections

#### 1. **Summary Cards** (Top Row)
Key metrics at a glance:
- **Total Tickets**: All tickets in system
- **Open Tickets**: Awaiting resolution (+ in progress count)
- **High Risk (P1-P2)**: Critical priority tickets
- **Closed Tickets**: Resolved issues
- **Average SLA**: Overall SLA performance
- **Oldest Open**: Days since oldest unresolved ticket

#### 2. **Priority Distribution** (Left Chart)
Bar chart showing tickets by priority level (P1-P5)
- P1: Red (Critical)
- P2: Orange (High)
- P3: Yellow (Medium)
- P4: Green (Low)
- P5: Blue (Minimal)

#### 3. **Status Distribution** (Right Chart)
Pie chart showing tickets by status:
- Open
- Closed
- In Progress

#### 4. **SLA Trend** (Bottom Left)
Line chart of average SLA over last 7 days
- Shows daily trends
- Helps identify SLA degradation

#### 5. **Regional Distribution** (Bottom Right)
Horizontal bar chart showing tickets by geographic region
- Helps identify regional hotspots
- Useful for resource allocation

#### 6. **Category Performance** (Table)
Table with metrics for each ticket category:
- **Total**: Total tickets in category
- **Closed**: Resolved tickets
- **Rate**: Closure rate percentage
- **Avg SLA**: Average SLA percentage

#### 7. **Assignment Group Workload** (Table)
Workload metrics per support team:
- **Total**: All assigned tickets
- **Open**: Unresolved tickets
- **Avg SLA**: Average SLA performance

Highlighting:
- Open tickets > 5: Shown in red (overloaded)
- SLA < 50%: Indicates underperformance

#### 8. **Oldest Open Tickets** (Table)
List of 5 oldest unresolved tickets
- **Ticket ID**: Link to ticket
- **Priority**: P1-P5 with color coding
- **Category**: Ticket type
- **Open Days**: Days since opened
  - Red if > 30 days (critical)
- **SLA %**: Current SLA percentage
- **Assigned To**: Support group

---

## 🔌 API Endpoints

The frontend uses the following backend API endpoints:

### Dashboard Endpoints

All endpoints require `Authorization: Bearer {token}` header.

#### Get Complete Dashboard Data
```
GET /api/dashboard/
Response: All dashboard data in one request
```

#### Get Summary Statistics
```
GET /api/dashboard/summary
Response: {
  "total_tickets": 100,
  "open_tickets": 45,
  "closed_tickets": 50,
  "in_progress_tickets": 5,
  "high_risk_tickets": 8,
  "average_sla_percentage": 78.5
}
```

#### Get Priority Distribution
```
GET /api/dashboard/priority-distribution
Response: {
  "distribution": {
    "P1": 8,
    "P2": 12,
    "P3": 35,
    "P4": 30,
    "P5": 15
  }
}
```

#### Get Status Distribution
```
GET /api/dashboard/status-distribution
Response: {
  "distribution": {
    "Open": 45,
    "Closed": 50,
    "In Progress": 5
  }
}
```

#### Get Region Distribution
```
GET /api/dashboard/region-distribution
Response: {
  "distribution": {
    "US-East": 30,
    "US-West": 25,
    "EU-Central": 20,
    "Asia-Pacific": 25
  }
}
```

#### Get Category Performance
```
GET /api/dashboard/category-performance
Response: {
  "categories": [
    {
      "category": "Network",
      "total": 25,
      "closed": 20,
      "average_sla": 82.5,
      "closure_rate": 80.0
    }
  ]
}
```

#### Get Assignment Group Workload
```
GET /api/dashboard/assignment-group-workload
Response: {
  "groups": [
    {
      "assignment_group": "Network-Support",
      "total_tickets": 30,
      "open_tickets": 12,
      "average_sla": 75.3
    }
  ]
}
```

#### Get SLA Trend
```
GET /api/dashboard/sla-trend?days=7
Response: {
  "trend": [
    {
      "date": "2024-01-20",
      "average_sla": 78.5,
      "ticket_count": 10
    }
  ]
}
```

#### Get Oldest Tickets
```
GET /api/dashboard/oldest-tickets?limit=10
Response: {
  "tickets": [
    {
      "id": 1,
      "ticket_id": "T001",
      "priority": "P1",
      "category": "Network",
      "open_days": 45,
      "sla_percentage": 65.3,
      "assignment_group": "Network-Support"
    }
  ]
}
```

---

## 🏗️ Project Structure

```
frontend/
├── package.json              # Dependencies
├── vite.config.js           # Build config
├── index.html               # HTML entry point
└── src/
    ├── main.jsx             # React entry point
    ├── App.jsx              # Main app component
    └── pages/
        ├── Dashboard.jsx    # Dashboard component
        └── Login.jsx        # Login component
```

### Key Files

#### `frontend/package.json`
Dependencies:
- **React 18.2**: UI library
- **Material-UI**: Component library
- **Recharts**: Charting library
- **Axios**: HTTP client
- **Vite**: Build tool

#### `frontend/src/App.jsx`
Main app component:
- Handles login/logout
- Manages authentication state
- Renders Dashboard or Login

#### `frontend/src/pages/Dashboard.jsx`
Full dashboard implementation:
- Fetches data from API
- Renders all metrics and charts
- Auto-refreshes every 30 seconds
- Error handling

#### `frontend/src/pages/Login.jsx`
Login page:
- Email/password form
- Stores JWT token
- Redirects to dashboard on success

---

## 🔧 Development

### Modify Dashboard

Edit `frontend/src/pages/Dashboard.jsx`:

1. **Add new chart:**
   ```jsx
   <ResponsiveContainer width="100%" height={300}>
     <BarChart data={your_data}>
       ...
     </BarChart>
   </ResponsiveContainer>
   ```

2. **Add new metric card:**
   ```jsx
   <StatCard
     title="Metric Name"
     value={value}
     icon={IconComponent}
     color="#color"
   />
   ```

3. **Changes hot-reload automatically**

### Modify Login

Edit `frontend/src/pages/Login.jsx`:
- Change demo credentials
- Adjust form styling
- Add password reset link

### Add API Call

Example - add new endpoint:
```jsx
const response = await axios.get(`${API_BASE}/dashboard/new-endpoint`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
setData(response.data);
```

---

## 🎨 Customization

### Theme Colors

Edit `frontend/src/main.jsx`:
```jsx
const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3',  // Change primary color
    },
    secondary: {
      main: '#f50057',  // Change secondary color
    },
  },
});
```

### Chart Colors

Edit `frontend/src/pages/Dashboard.jsx`:
```jsx
const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1'];
const PRIORITY_COLORS = {
  P1: '#ff4444',  // Customize priority colors
  P2: '#ff9800',
  // ...
};
```

---

## 🐛 Troubleshooting

### "Cannot connect to http://localhost:8000"
**Solution:** Ensure backend is running:
```bash
run.bat  # Windows
bash run.sh  # Unix
```

### "Failed to load dashboard data"
**Solution:** 
1. Check token is valid (login again)
2. Check backend is responding: `curl http://localhost:8000/health`
3. Check CORS is enabled in backend

### Charts not showing
**Solution:**
1. Open browser console (F12)
2. Check for errors
3. Verify API endpoints are working:
   ```bash
   curl http://localhost:8000/api/dashboard/summary
   ```

### Port 3000 already in use
**Solution:** Change port in `frontend/vite.config.js`:
```jsx
server: {
  port: 3001,  // Change to different port
}
```

---

## 📦 Build for Production

```bash
cd frontend
npm run build
```

Creates optimized build in `frontend/dist/`

Deploy to:
- Azure Static Web Apps
- Vercel
- Netlify
- Any static host

---

## 🔄 Data Refresh

Dashboard auto-refreshes every 30 seconds. To change:

Edit `frontend/src/pages/Dashboard.jsx`:
```jsx
useEffect(() => {
  fetchData();
  const interval = setInterval(fetchData, 30000);  // Change milliseconds
  return () => clearInterval(interval);
}, []);
```

---

## 📚 Next Steps

1. ✅ Install and run frontend
2. ✅ Login with demo account
3. ✅ Explore dashboard metrics
4. → Upload sample tickets to see data
5. → Implement predictions (Phase 5)

---

## Support

For issues:
1. Check troubleshooting section above
2. Review browser console (F12)
3. Check backend logs
4. Verify credentials and permissions

Enjoy your incident dashboard! 🎯
