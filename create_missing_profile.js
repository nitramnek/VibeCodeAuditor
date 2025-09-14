// Create missing profile for kenwanguka@gmail.com
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client with service role key for admin access
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function createMissingProfile() {
  console.log('=== Creating Missing Profile ===');
  
  // First, let's get the user ID for kenwanguka@gmail.com
  console.log('\n1. Getting user ID for kenwanguka@gmail.com...');
  
  try {
    // Get user by email
    const { data: userData, error: userError } = await supabase.auth.admin.listUsers();
    
    if (userError) {
      console.error('❌ Error fetching users:', userError.message);
      return;
    }
    
    // Find the user with email kenwanguka@gmail.com
    const user = userData.users.find(u => u.email === 'kenwanguka@gmail.com');
    
    if (!user) {
      console.error('❌ User kenwanguka@gmail.com not found in auth.users');
      return;
    }
    
    console.log('✅ User found:', user.id, user.email);
    
    // Check if profile already exists
    console.log('\n2. Checking if profile already exists...');
    const { data: existingProfile, error: profileError } = await supabase
      .from('profiles')
      .select('id, email')
      .eq('id', user.id)
      .single();
    
    if (profileError && profileError.code !== 'PGRST116') {
      console.error('❌ Error checking profile:', profileError.message);
      return;
    }
    
    if (existingProfile) {
      console.log('✅ Profile already exists:', existingProfile);
      return;
    }
    
    console.log('❌ Profile does not exist, creating one...');
    
    // Create the profile
    console.log('\n3. Creating profile...');
    const profileData = {
      id: user.id,
      email: user.email,
      full_name: user.user_metadata?.full_name || user.email,
      role_id: 'user' // Default role
    };
    
    const { data: newProfile, error: createError } = await supabase
      .from('profiles')
      .insert(profileData)
      .select()
      .single();
    
    if (createError) {
      console.error('❌ Error creating profile:', createError.message);
      console.log('Profile data:', profileData);
      return;
    }
    
    console.log('✅ Profile created successfully:', newProfile);
    
    // Verify the profile was created
    console.log('\n4. Verifying profile creation...');
    const { data: verifiedProfile, error: verifyError } = await supabase
      .from('profiles')
      .select('id, email, full_name, role_id')
      .eq('id', user.id)
      .single();
    
    if (verifyError) {
      console.error('❌ Verification failed:', verifyError.message);
    } else {
      console.log('✅ Profile verified:', verifiedProfile);
    }
    
  } catch (err) {
    console.error('❌ Unexpected error:', err.message);
  }
  
  console.log('\n=== Process Complete ===');
}

createMissingProfile().catch(console.error);
