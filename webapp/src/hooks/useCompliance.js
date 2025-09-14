import { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { 
  complianceFrameworksApi, 
  complianceAuditsApi, 
  riskAssessmentsApi, 
  policiesApi,
  complianceAnalyticsApi 
} from '../services/complianceApi';

export const useCompliance = () => {
  const [complianceData, setComplianceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchComplianceData();
  }, []);

  const fetchComplianceData = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        setError('User not authenticated');
        return;
      }

      // Use the analytics API to get comprehensive dashboard data
      const dashboardData = await complianceAnalyticsApi.getDashboardData(user.id);
      setComplianceData(dashboardData);

    } catch (err) {
      console.error('Error fetching compliance data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createFramework = async (frameworkData) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('User not authenticated');

      const data = await complianceFrameworksApi.create({
        ...frameworkData,
        user_id: user.id
      });

      // Refresh data
      await fetchComplianceData();
      return data;
    } catch (err) {
      console.error('Error creating framework:', err);
      throw err;
    }
  };

  const updateFramework = async (id, updates) => {
    try {
      const data = await complianceFrameworksApi.update(id, updates);
      
      // Refresh data
      await fetchComplianceData();
      return data;
    } catch (err) {
      console.error('Error updating framework:', err);
      throw err;
    }
  };

  const deleteFramework = async (id) => {
    try {
      await complianceFrameworksApi.delete(id);
      
      // Refresh data
      await fetchComplianceData();
    } catch (err) {
      console.error('Error deleting framework:', err);
      throw err;
    }
  };

  const createAudit = async (auditData) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('User not authenticated');

      const data = await complianceAuditsApi.create({
        ...auditData,
        user_id: user.id
      });

      // Refresh data
      await fetchComplianceData();
      return data;
    } catch (err) {
      console.error('Error creating audit:', err);
      throw err;
    }
  };

  const createRiskAssessment = async (assessmentData) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('User not authenticated');

      const data = await riskAssessmentsApi.create({
        ...assessmentData,
        user_id: user.id,
        last_updated: new Date().toISOString()
      });

      // Refresh data
      await fetchComplianceData();
      return data;
    } catch (err) {
      console.error('Error creating risk assessment:', err);
      throw err;
    }
  };

  const createPolicy = async (policyData) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('User not authenticated');

      const data = await policiesApi.create({
        ...policyData,
        user_id: user.id,
        last_reviewed: new Date().toISOString()
      });

      // Refresh data
      await fetchComplianceData();
      return data;
    } catch (err) {
      console.error('Error creating policy:', err);
      throw err;
    }
  };

  return {
    complianceData,
    loading,
    error,
    refetch: fetchComplianceData,
    createFramework,
    updateFramework,
    deleteFramework,
    createAudit,
    createRiskAssessment,
    createPolicy
  };
};
