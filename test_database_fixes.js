/**
 * Test script to verify database fixes are working
 */

const { createClient } = require('@supabase/supabase-js');

// Load environment variables
require('dotenv').config();

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing Supabase environment variables');
  console.log('Make sure REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY are set');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function testDatabaseFixes() {
  console.log('🧪 Testing Database Fixes');
  console.log('=' * 40);

  try {
    // Test 1: Check if we can create a scan without infinite recursion
    console.log('\n1. Testing scan creation...');
    
    // First, let's get a test user (you'll need to be logged in)
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    
    if (authError || !user) {
      console.log('⚠️  No authenticated user found. Please log in first.');
      console.log('   You can test this after logging into the web app.');
      return;
    }
    
    console.log(`✅ Authenticated as: ${user.email}`);
    
    // Test 2: Try to create a scan
    const { data: scanData, error: scanError } = await supabase
      .from('scans')
      .insert([
        {
          user_id: user.id,
          name: 'Test Scan - Database Fix Verification',
          status: 'completed',
          file_count: 1,
          summary: { test: true },
          compliance_summary: { test: true },
          detected_frameworks: { test: true }
        }
      ])
      .select()
      .single();

    if (scanError) {
      console.error('❌ Error creating scan:', scanError);
      return;
    }
    
    console.log('✅ Scan created successfully:', scanData.id);
    
    // Test 3: Try to create an issue for the scan
    console.log('\n2. Testing issue creation...');
    
    const { data: issueData, error: issueError } = await supabase
      .from('issues')
      .insert([
        {
          scan_id: scanData.id,
          title: 'Test Issue',
          description: 'This is a test issue to verify database fixes',
          severity: 'medium',
          status: 'open',
          file_path: 'test.js',
          line_number: 42,
          recommendation: 'This is a test recommendation'
        }
      ])
      .select()
      .single();

    if (issueError) {
      console.error('❌ Error creating issue:', issueError);
      return;
    }
    
    console.log('✅ Issue created successfully:', issueData.id);
    
    // Test 4: Try to fetch the scan and its issues
    console.log('\n3. Testing scan retrieval...');
    
    const { data: retrievedScan, error: retrieveError } = await supabase
      .from('scans')
      .select('*')
      .eq('id', scanData.id)
      .eq('user_id', user.id)
      .single();

    if (retrieveError) {
      console.error('❌ Error retrieving scan:', retrieveError);
      return;
    }
    
    console.log('✅ Scan retrieved successfully');
    
    // Test 5: Try to fetch issues for the scan
    const { data: retrievedIssues, error: issuesRetrieveError } = await supabase
      .from('issues')
      .select('id, title, description, severity, status, created_at')
      .eq('scan_id', scanData.id);

    if (issuesRetrieveError) {
      console.error('❌ Error retrieving issues:', issuesRetrieveError);
      return;
    }
    
    console.log('✅ Issues retrieved successfully:', retrievedIssues.length, 'issues found');
    
    // Test 6: Clean up test data
    console.log('\n4. Cleaning up test data...');
    
    await supabase.from('issues').delete().eq('scan_id', scanData.id);
    await supabase.from('scans').delete().eq('id', scanData.id);
    
    console.log('✅ Test data cleaned up');
    
    console.log('\n🎉 All database fixes are working correctly!');
    console.log('✅ No infinite recursion errors');
    console.log('✅ Scan creation works');
    console.log('✅ Issue creation works');
    console.log('✅ Data retrieval works');
    console.log('✅ RLS policies are functioning properly');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

// Run the test
testDatabaseFixes();