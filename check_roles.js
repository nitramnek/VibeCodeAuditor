// Check what roles exist in the database
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function checkRoles() {
  console.log('=== Checking Roles ===');
  
  try {
    // Check if roles table exists and get available roles
    console.log('\n1. Checking roles table...');
    const { data: roles, error: rolesError } = await supabase
      .from('roles')
      .select('id, name, description')
      .order('name');
    
    if (rolesError) {
      console.error('❌ Error fetching roles:', rolesError.message);
      console.log('This suggests the roles table might not exist or have data');
      
      // Check if we can create a default role
      console.log('\n2. Trying to create default roles...');
      const defaultRoles = [
        { name: 'user', description: 'Regular user' },
        { name: 'admin', description: 'Administrator' },
        { name: 'auditor', description: 'Security auditor' }
      ];
      
      for (const role of defaultRoles) {
        const { error: insertError } = await supabase
          .from('roles')
          .insert(role)
          .select();
        
        if (insertError) {
          console.log(`❌ Error creating role ${role.name}:`, insertError.message);
        } else {
          console.log(`✅ Created role: ${role.name}`);
        }
      }
      
      // Try to get roles again
      const { data: newRoles, error: newRolesError } = await supabase
        .from('roles')
        .select('id, name, description')
        .order('name');
      
      if (newRolesError) {
        console.error('❌ Still cannot fetch roles:', newRolesError.message);
      } else {
        console.log('✅ Available roles:', newRoles);
      }
      
    } else {
      console.log('✅ Available roles:', roles);
      
      // Find the user role
      const userRole = roles.find(r => r.name === 'user');
      if (userRole) {
        console.log('✅ User role found:', userRole);
      } else {
        console.log('❌ User role not found in roles table');
      }
    }
    
  } catch (err) {
    console.error('❌ Unexpected error:', err.message);
  }
  
  console.log('\n=== Process Complete ===');
}

checkRoles().catch(console.error);
