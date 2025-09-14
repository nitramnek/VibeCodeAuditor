// Create profile directly using known user ID
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function createProfileDirect() {
  console.log('=== Creating Profile Directly ===');
  
  const userId = '289c36cf-8779-4e49-bcfe-b829d0899472';
  const userEmail = 'kenwanguka@gmail.com';
  
  console.log('Using user ID:', userId);
  console.log('Using email:', userEmail);
  
  try {
    // Check if profile already exists
    console.log('\n1. Checking if profile already exists...');
    const { data: existingProfile, error: profileError } = await supabase
      .from('profiles')
      .select('id, email, full_name, role_id')
      .eq('id', userId)
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
    console.log('\n2. Creating profile...');
    const profileData = {
      id: userId,
      email: userEmail,
      full_name: userEmail, // Use email as full name
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
      console.log('Error details:', createError);
      return;
    }
    
    console.log('✅ Profile created successfully:', newProfile);
    
    // Verify the profile was created
    console.log('\n3. Verifying profile creation...');
    const { data: verifiedProfile, error: verifyError } = await supabase
      .from('profiles')
      .select('id, email, full_name, role_id')
      .eq('id', userId)
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

createProfileDirect().catch(console.error);
