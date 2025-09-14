// Check the actual roles table structure
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function checkRolesStructure() {
  console.log('=== Checking Roles Structure ===');
  
  try {
    // Check the actual roles table
    console.log('\n1. Checking roles table structure...');
    const { data: roles, error: rolesError } = await supabase
      .from('roles')
      .select('*')
      .limit(5);
    
    if (rolesError) {
      console.error('❌ Error fetching roles:', rolesError.message);
    } else {
      console.log('✅ Roles table data:', roles);
    }
    
    // Check user_roles table
    console.log('\n2. Checking user_roles table...');
    const { data: userRoles, error: userRolesError } = await supabase
      .from('user_roles')
      .select('*')
      .limit(5);
    
    if (userRolesError) {
      console.error('❌ Error fetching user_roles:', userRolesError.message);
    } else {
      console.log('✅ User roles data:', userRoles);
    }
    
    // Check the specific user role mentioned
    console.log('\n3. Checking specific user role...');
    const roleId = '196154e0-ecd8-4dd3-ac3d-e5ab61d81245';
    const { data: specificRole, error: specificError } = await supabase
      .from('roles')
      .select('*')
      .eq('id', roleId)
      .single();
    
    if (specificError) {
      console.error('❌ Error fetching specific role:', specificError.message);
    } else {
      console.log('✅ Specific role found:', specificRole);
    }
    
  } catch (err) {
    console.error('❌ Unexpected error:', err.message);
  }
  
  console.log('\n=== Process Complete ===');
}

checkRolesStructure().catch(console.error);
