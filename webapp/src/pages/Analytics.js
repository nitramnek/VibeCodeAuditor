import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { fetchAnalyticsData } from '../services/analyticsService';
import LineChart from '../components/Analytics/LineChart';
import BarChart from '../components/Analytics/BarChart';
import PieChart from '../components/Analytics/PieChart';
import MetricCard from '../components/Analytics/MetricCard';
import DataTable from '../components/Analytics/DataTable';

const Analytics = () => {
  const [dateRange, setDateRange] = useState('30d');
  const { data, isLoading, error, refetch } = useQuery(
    ['analyticsData', dateRange],
    () => fetchAnalyticsData(dateRange),
    {
      refetchInterval: 60000, // Refetch every 60 seconds for real-time updates
    }
  );

  useEffect(() => {
    refetch();
  }, [dateRange, refetch]);

  if (isLoading) return <div className="p-6">Loading analytics data...</div>;
  if (error) return <div className="p-6">Error loading analytics data: {error.message}</div>;

  // Transform Supabase data to component format
  const transformedData = {
    totalScans: data.scanAnalytics?.length || 0,
    criticalIssues: data.scanAnalytics?.reduce((sum, scan) => sum + (scan.critical_issues || 0), 0) || 0,
    resolvedIssues: data.scanAnalytics?.reduce((sum, scan) => sum + (scan.resolved_issues || 0), 0) || 0,
    complianceScore: data.complianceAnalytics?.[0]?.average_score || 0,
    securityScore: data.scanAnalytics?.reduce((sum, scan) => sum + (scan.security_score || 0), 0) / (data.scanAnalytics?.length || 1) || 0,
    trendData: data.scanAnalytics?.map(scan => ({
      date: scan.scan_date,
      value: scan.total_issues || 0
    })) || [],
    issueDistribution: [
      { name: 'Critical', value: data.scanAnalytics?.reduce((sum, scan) => sum + (scan.critical_issues || 0), 0) || 0 },
      { name: 'High', value: data.scanAnalytics?.reduce((sum, scan) => sum + (scan.high_issues || 0), 0) || 0 },
      { name: 'Medium', value: data.scanAnalytics?.reduce((sum, scan) => sum + (scan.medium_issues || 0), 0) || 0 },
      { name: 'Low', value: data.scanAnalytics?.reduce((sum, scan) => sum + (scan.low_issues || 0), 0) || 0 },
    ],
    complianceBreakdown: data.complianceAnalytics?.map(framework => ({
      name: framework.framework_name,
      value: framework.average_score || 0
    })) || [],
    recentScans: data.scanAnalytics?.slice(0, 10).map(scan => ({
      id: scan.scan_id,
      name: scan.scan_name || 'Unnamed Scan',
      status: scan.status || 'Unknown',
      issues: scan.total_issues || 0,
      date: scan.scan_date
    })) || [],
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Analytics Dashboard</h1>

      {/* Date Range Selector */}
      <div className="mb-6">
        <label htmlFor="dateRange" className="mr-4 font-medium">
          Date Range:
        </label>
        <select
          id="dateRange"
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          className="border border-gray-300 rounded px-3 py-1"
        >
          <option value="7d">Last 7 days</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
          <option value="365d">Last 12 months</option>
        </select>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8">
        <MetricCard title="Total Scans" value={transformedData.totalScans} />
        <MetricCard title="Critical Issues" value={transformedData.criticalIssues} />
        <MetricCard title="Resolved Issues" value={transformedData.resolvedIssues} />
        <MetricCard title="Compliance Score" value={`${Math.round(transformedData.complianceScore)}%`} />
        <MetricCard title="Security Score" value={`${Math.round(transformedData.securityScore)}%`} />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <LineChart data={transformedData.trendData} title="Scan Trends Over Time" />
        <BarChart data={transformedData.issueDistribution} title="Issue Distribution" />
        <PieChart data={transformedData.complianceBreakdown} title="Compliance Breakdown" />
      </div>

      {/* Data Table */}
      <div>
        <DataTable data={transformedData.recentScans} title="Recent Scans" />
      </div>
    </div>
  );
};

export default Analytics;
