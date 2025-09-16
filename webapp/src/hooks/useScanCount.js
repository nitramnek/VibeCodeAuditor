import { useState, useEffect } from 'react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';

export const useScanCount = () => {
  const [scanCount, setScanCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isSupabaseConfigured()) {
      setScanCount(0);
      setLoading(false);
      return;
    }

    const fetchScanCount = async () => {
      try {
        const {
          data: { user },
        } = await supabase.auth.getUser();

        if (!user) {
          setScanCount(0);
          setLoading(false);
          return;
        }

        // Fetch count of scans for the user
        const { count, error } = await supabase
          .from('scans')
          .select('*', { count: 'exact', head: true })
          .eq('user_id', user.id);

        if (error) {
          console.error('Error fetching scan count:', error);
          setScanCount(0);
        } else {
          setScanCount(count || 0);
        }
      } catch (err) {
        console.error('Unexpected error fetching scan count:', err);
        setScanCount(0);
      }
      setLoading(false);
    };

    fetchScanCount();

    // Set up real-time subscription for scan count updates
    const channel = supabase
      .channel('scan-count-updates')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'scans',
        },
        (payload) => {
          // Refetch count when scans table changes
          fetchScanCount();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  return { scanCount, loading };
};
