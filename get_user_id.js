// Get user ID for kenwanguka@gmail.com using auth API
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function getUserID() {
  console.log('=== Getting User ID ===');
  
  try {
    // Try to sign in to get the user ID (this will fail but give us error details)
    const { data, error } = await supabase.auth.signInWithPassword({
      email: 'kenwanguka@gmail.com',
      password: 'temporary_password' // This will fail
    });
    
    if (error) {
      console.log('Sign in failed (expected):', error.message);
      
      // The error might contain user information or we can try to get user by email
      console.log('\nTrying to get user information...');
      
      // Use the admin API if available, or try a different approach
      try {
        // This might work with the anon key for public auth operations
        const { data: userData, error: userError } = await supabase.auth.getUser();
        
        if (userError) {
          console.log('Cannot get current user:', userError.message);
        } else {
          console.log('Current user:', userData.user);
        }
      } catch (err) {
        console.log('Error getting user:', err.message);
      }
    } else {
      console.log('Unexpected success:', data);
    }
    
  } catch (err) {
    console.error('Unexpected error:', err.message);
  }
  
  console.log('\n=== Process Complete ===');
}

getUserID().catch(console.error);
