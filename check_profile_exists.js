// Check if the profile exists with a simple query
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function checkProfileExists() {
  console.log('=== Checking Profile Existence ===');
  
  const userId = '289c36cf-8779-4e49-bcfe-b829d0899472';
  
  try {
    // First, check if we can query the profiles table at all
    console.log('\n1. Checking profiles table accessibility...');
    const { data: allProfiles, error: tableError } = await supabase
      .from('profiles')
      .select('count')
      .single();

    if (tableError) {
      console.error('❌ Cannot access profiles table:', tableError.message);
      return;
    } else {
      console.log('✅ Profiles table is accessible');
    }

    // Try a simple query without .single() to see what we get
    console.log('\n2. Trying simple query without .single()...');
    const { data: profiles, error: simpleError } = await supabase
      .from('profiles')
      .select('id, email, role_id')
      .eq('id', userId);

    if (simpleError) {
      console.error('❌ Simple query error:', simpleError.message);
    } else {
      console.log('✅ Simple query result:', profiles);
      if (profiles && profiles.length > 0) {
        console.log('✅ Profile found:', profiles[0]);
      } else {
        console.log('❌ No profile found for user ID:', userId);
      }
    }

    // Check if the user exists in auth.users
    console.log('\n3. Checking auth user existence...');
    try {
      // This might require admin privileges, but let's try
      const { data: authUsers, error: authError } = await supabase.auth.admin.listUsers();
      if (authError) {
        console.log('Cannot list auth users (requires admin):', authError.message);
      } else {
        const user = authUsers.users.find(u => u.id === userId);
        if (user) {
          console.log('✅ Auth user found:', user.email);
        } else {
          console.log('❌ Auth user not found with ID:', userId);
        }
      }
    } catch (authErr) {
      console.log('Auth check failed (expected without admin):', authErr.message);
    }

  } catch (err) {
    console.error('❌ Unexpected error:', err.message);
  }
  
  console.log('\n=== Check Complete ===');
}

checkProfileExists().catch(console.error);
