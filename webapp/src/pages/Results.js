// webapp/src/pages/Results.js
import React, { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { supabase } from "../lib/supabase";
import {
  FileText,
  AlertTriangle,
  CheckCircle,
  Clock,
} from "lucide-react";

const Results = () => {
  const { scanId } = useParams(); // get /results/:scanId
  const location = useLocation();
  const [scan, setScan] = useState(null);
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Get fallback data from navigation state
    const fallbackIssues = location.state?.fallbackIssues || [];
    const fetchResults = async () => {
      setLoading(true);
      try {
        const {
          data: { user },
        } = await supabase.auth.getUser();

        if (!user) {
          setLoading(false);
          return;
        }

        // fetch scan details
        const { data: scanData, error: scanError } = await supabase
          .from("scans")
          .select("*")
          .eq("id", scanId)
          .eq("user_id", user.id)
          .single();

        if (scanError) {
          console.error("Error fetching scan:", scanError);
          setLoading(false);
          return;
        }
        setScan(scanData);

        // fetch related issues
        const { data: issuesData, error: issuesError } = await supabase
          .from("issues")
          .select("id, title, description, severity, status, created_at")
          .eq("scan_id", scanId)
          .order("created_at", { ascending: false });

        if (issuesError) {
          console.error("Error fetching issues:", issuesError);
          // Use fallback issues if database fetch fails
          if (fallbackIssues.length > 0) {
            console.log("Using fallback issues from navigation state");
            const formattedFallbackIssues = fallbackIssues.map((issue, index) => ({
              id: `fallback-${index}`,
              title: issue.description || issue.message || 'Security Issue',
              description: issue.recommendation || issue.description || 'No description available',
              severity: issue.severity || 'medium',
              status: 'open',
              created_at: new Date().toISOString()
            }));
            setIssues(formattedFallbackIssues);
          } else {
            setIssues([]);
          }
        } else {
          const dbIssues = issuesData || [];
          // If no database issues but we have fallback issues, use fallback
          if (dbIssues.length === 0 && fallbackIssues.length > 0) {
            console.log("No database issues found, using fallback issues");
            const formattedFallbackIssues = fallbackIssues.map((issue, index) => ({
              id: `fallback-${index}`,
              title: issue.description || issue.message || 'Security Issue',
              description: issue.recommendation || issue.description || 'No description available',
              severity: issue.severity || 'medium',
              status: 'open',
              created_at: new Date().toISOString()
            }));
            setIssues(formattedFallbackIssues);
          } else {
            setIssues(dbIssues);
          }
        }

        // log in audit_logs (convert UUID to string for resource_id)
        try {
          await supabase.from("audit_logs").insert([
            {
              user_id: user.id,
              resource_id: null, // Set to null since we're using UUID scans now
              action: "view_scan_issues",
            },
          ]);
        } catch (auditError) {
          console.error("Error logging audit:", auditError);
          // Don't fail the whole operation if audit logging fails
        }
      } catch (err) {
        console.error("Unexpected error:", err);
      }
      setLoading(false);
    };

    if (scanId) fetchResults();
  }, [scanId, location.state?.fallbackIssues]);

  if (loading) {
    return <div className="p-6">Loading results...</div>;
  }

  if (!scan) {
    return (
      <div className="p-6">
        <p className="text-gray-600">Scan not found.</p>
        <button
          onClick={() => navigate("/scan-results")}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
        >
          Back to Scan Results
        </button>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-semibold">{scan.name || "Untitled Scan"}</h1>
          <p className="text-sm text-gray-500">
            {new Date(scan.created_at).toLocaleString()}
          </p>
        </div>
        <div
          className={`px-3 py-1 rounded text-sm font-medium ${
            scan.status === "completed"
              ? "bg-green-100 text-green-700"
              : scan.status === "failed"
              ? "bg-red-100 text-red-700"
              : "bg-yellow-100 text-yellow-700"
          }`}
        >
          {scan.status}
        </div>
      </div>

      <h2 className="text-xl font-medium mb-4 flex items-center">
        <FileText className="mr-2" size={20} /> Issues ({issues.length})
      </h2>

      {issues.length === 0 ? (
        <p className="text-gray-600">No issues found for this scan 🎉</p>
      ) : (
        <div className="space-y-4">
          {issues.map((issue) => (
            <div
              key={issue.id}
              className="border rounded-lg p-4 shadow-sm hover:shadow-md transition"
            >
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium">{issue.title}</h3>
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${
                    issue.severity === "critical"
                      ? "bg-red-100 text-red-700"
                      : issue.severity === "high"
                      ? "bg-orange-100 text-orange-700"
                      : issue.severity === "medium"
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-gray-100 text-gray-700"
                  }`}
                >
                  {issue.severity}
                </span>
              </div>
              <p className="text-sm text-gray-600 mt-1">{issue.description}</p>

              <div className="flex items-center mt-2 text-sm space-x-4">
                <span className="flex items-center">
                  {issue.status === "open" ? (
                    <AlertTriangle size={16} className="mr-1 text-red-600" />
                  ) : issue.status === "in_progress" ? (
                    <Clock size={16} className="mr-1 text-yellow-600" />
                  ) : (
                    <CheckCircle size={16} className="mr-1 text-green-600" />
                  )}
                  {issue.status}
                </span>
                <span className="text-gray-500">
                  {new Date(issue.created_at).toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      <button
        onClick={() => navigate("/scan-results")}
        className="mt-6 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
      >
        Back to Scan Results
      </button>
    </div>
  );
};

export default Results;
