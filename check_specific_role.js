// Check the specific role by ID
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function checkSpecificRole() {
  console.log('=== Checking Specific Role ===');
  
  const roleId = 'ac4c17be-fdb2-4e45-bcc4-96fe27b3be64';
  
  try {
    // Check if this role exists in the roles table
    console.log('\n1. Checking role in roles table...');
    const { data: role, error: roleError } = await supabase
      .from('roles')
      .select('*')
      .eq('id', roleId)
      .single();
    
    if (roleError) {
      console.log('❌ Role not found in roles table:', roleError.message);
    } else {
      console.log('✅ Role found:', role);
    }
    
    // Check if there's a different table structure
    console.log('\n2. Checking all tables...');
    const { data: tables, error: tablesError } = await supabase
      .from('pg_tables')
      .select('tablename')
      .eq('schemaname', 'public');
    
    if (tablesError) {
      console.log('Cannot query pg_tables:', tablesError.message);
    } else {
      console.log('Available tables:', tables.map(t => t.tablename));
    }
    
    // Try a direct query to see what's available
    console.log('\n3. Testing direct profile query...');
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('id, email, role_id')
      .eq('id', '289c36cf-8779-4e49-bcfe-b829d0899472')
      .single();
    
    if (profileError) {
      console.log('❌ Profile query failed:', profileError.message);
    } else {
      console.log('✅ Profile query successful:', profile);
    }
    
  } catch (err) {
    console.error('❌ Unexpected error:', err.message);
  }
  
  console.log('\n=== Process Complete ===');
}

checkSpecificRole().catch(console.error);
