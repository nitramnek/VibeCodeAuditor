import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import {
  FileText,
  Eye,
  Calendar,
  Shield,
  Search,
  Filter,
  X,
  SortAsc
} from 'lucide-react';

const ScanResults = () => {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchScans = async () => {
      setLoading(true);
      try {
        const {
          data: { user },
        } = await supabase.auth.getUser();

        if (!user) {
          setLoading(false);
          return;
        }

        // Fetch all scans for the user
        const { data: scansData, error } = await supabase
          .from('scans')
          .select('*')
          .eq('user_id', user.id)
          .order('created_at', { ascending: false });

        if (error) {
          console.error('Error fetching scans:', error);
          setScans([]);
        } else {
          setScans(scansData || []);
        }
      } catch (err) {
        console.error('Unexpected error:', err);
        setScans([]);
      }
      setLoading(false);
    };

    fetchScans();
  }, []);

  // Filter and sort scans
  const filteredAndSortedScans = useMemo(() => {
    let filtered = scans.filter((scan) => {
      // Search filter
      const matchesSearch = searchTerm === '' ||
        (scan.name || '').toLowerCase().includes(searchTerm.toLowerCase());

      // Status filter
      const matchesStatus = statusFilter === 'all' || scan.status === statusFilter;

      return matchesSearch && matchesStatus;
    });

    // Sort scans
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.created_at) - new Date(a.created_at);
        case 'oldest':
          return new Date(a.created_at) - new Date(b.created_at);
        case 'most-issues':
          return (b.total_issues || 0) - (a.total_issues || 0);
        case 'least-issues':
          return (a.total_issues || 0) - (b.total_issues || 0);
        default:
          return 0;
      }
    });

    return filtered;
  }, [scans, searchTerm, statusFilter, sortBy]);

  const clearFilters = () => {
    setSearchTerm('');
    setStatusFilter('all');
    setSortBy('newest');
  };



  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'in_progress': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading scan results...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Shield className="mr-3 h-8 w-8 text-blue-600" />
            Scan Results
          </h1>
          <p className="mt-2 text-gray-600">
            View and manage your security scan results
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-gray-900">{scans.length}</div>
          <div className="text-sm text-gray-500">Total Scans</div>
        </div>
      </div>

      {/* Search and Filter Controls */}
      {scans.length > 0 && (
        <div className="bg-white rounded-xl shadow-modern p-6 mb-6">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Input */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search scans by name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Status Filter */}
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="pl-10 pr-8 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
              >
                <option value="all">All Status</option>
                <option value="completed">Completed</option>
                <option value="failed">Failed</option>
                <option value="in_progress">In Progress</option>
              </select>
            </div>

            {/* Sort Options */}
            <div className="relative">
              <SortAsc className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="pl-10 pr-8 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="most-issues">Most Issues</option>
                <option value="least-issues">Least Issues</option>
              </select>
            </div>

            {/* Clear Filters */}
            {(searchTerm || statusFilter !== 'all' || sortBy !== 'newest') && (
              <button
                onClick={clearFilters}
                className="inline-flex items-center px-4 py-3 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <X className="mr-2 h-4 w-4" />
                Clear Filters
              </button>
            )}
          </div>

          {/* Results Summary */}
          <div className="mt-4 flex items-center justify-between text-sm text-gray-600">
            <span>
              Showing {filteredAndSortedScans.length} of {scans.length} scans
            </span>
            {(searchTerm || statusFilter !== 'all') && (
              <span className="text-blue-600">
                {searchTerm && `Search: "${searchTerm}"`}
                {searchTerm && statusFilter !== 'all' && ' • '}
                {statusFilter !== 'all' && `Status: ${statusFilter}`}
              </span>
            )}
          </div>
        </div>
      )}

      {scans.length === 0 ? (
        <div className="bg-white rounded-xl shadow-modern p-12 text-center">
          <FileText className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h3 className="text-xl font-medium text-gray-900 mb-2">No Scans Yet</h3>
          <p className="text-gray-600 mb-6">
            Start your first security scan to see results here.
          </p>
          <button
            onClick={() => navigate('/scanner')}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            Start Scanning
          </button>
        </div>
      ) : filteredAndSortedScans.length === 0 ? (
        <div className="bg-white rounded-xl shadow-modern p-12 text-center">
          <Search className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h3 className="text-xl font-medium text-gray-900 mb-2">No Results Found</h3>
          <p className="text-gray-600 mb-6">
            No scans match your current filters. Try adjusting your search criteria.
          </p>
          <button
            onClick={clearFilters}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            Clear Filters
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredAndSortedScans.map((scan) => (
            <div
              key={scan.id}
              className="bg-white rounded-xl shadow-modern p-6 hover:shadow-modern-md transition-all duration-200 cursor-pointer"
              onClick={() => navigate(`/results/${scan.id}`)}
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {scan.name || 'Untitled Scan'}
                  </h3>
                  <div className="flex items-center text-sm text-gray-500 space-x-4">
                    <span className="flex items-center">
                      <Calendar className="mr-1 h-4 w-4" />
                      {new Date(scan.created_at).toLocaleDateString()}
                    </span>
                    <span className="flex items-center">
                      <FileText className="mr-1 h-4 w-4" />
                      {scan.file_count || 0} files
                    </span>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(scan.status)}`}>
                    {scan.status}
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/results/${scan.id}`);
                    }}
                    className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                  >
                    <Eye className="mr-2 h-4 w-4" />
                    View Results
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{scan.critical_issues || 0}</div>
                  <div className="text-xs text-gray-500">Critical</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{scan.high_issues || 0}</div>
                  <div className="text-xs text-gray-500">High</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">{scan.medium_issues || 0}</div>
                  <div className="text-xs text-gray-500">Medium</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{scan.low_issues || 0}</div>
                  <div className="text-xs text-gray-500">Low</div>
                </div>
              </div>

              <div className="flex justify-between items-center text-sm text-gray-600">
                <span>Total Issues: {scan.total_issues || 0}</span>
                <span className="text-blue-600 hover:text-blue-800 cursor-pointer">
                  Click to view details →
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ScanResults;
