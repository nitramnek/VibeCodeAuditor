// Test authentication flow
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found. Please set REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY environment variables.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testAuthFlow() {
  console.log('Testing authentication flow...');
  
  // Try to sign in
  const { data, error } = await supabase.auth.signInWithPassword({
    email: 'kenwanguka@gmail.com',
    password: 'your_password_here' // Replace with actual password
  });
  
  if (error) {
    console.error('Sign in error:', error);
    return;
  }
  
  console.log('Sign in successful:', data);
  
  // Fetch user profile
  if (data.user) {
    const { data: profileData, error: profileError } = await supabase
      .from('profiles')
      .select(`
        id,
        email,
        role_id,
        roles (name, description)
      `)
      .eq('id', data.user.id)
      .single();
      
    if (profileError) {
      console.error('Profile fetch error:', profileError);
    } else {
      console.log('Profile fetched successfully:', profileData);
    }
  }
}

