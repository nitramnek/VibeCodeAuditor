// Debug authentication flow
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

console.log('Supabase URL:', supabaseUrl);
console.log('Supabase Anon Key:', supabaseAnonKey ? '*** (set)' : 'Not set');

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found. Please set REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY environment variables.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Add error handling to see all output
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  process.exit(1);
});

async function debugAuthFlow() {
  console.log('\n=== Debugging Authentication Flow ===');
  
  // Test 1: Check if we can connect to Supabase
  console.log('\n1. Testing Supabase connection...');
  try {
    const { data, error } = await supabase.from('profiles').select('count').limit(1);
    if (error) {
      console.error('❌ Connection test failed:', error.message);
    } else {
      console.log('✅ Connection test successful');
    }
  } catch (err) {
    console.error('❌ Connection test error:', err.message);
  }

  // Test 2: Try to sign in (this will fail without proper password)
  console.log('\n2. Testing sign-in (will fail without password)...');
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: 'kenwanguka@gmail.com',
      password: 'test_password' // This will likely fail
    });
    
    if (error) {
      console.log('❌ Sign in failed (expected):', error.message);
      console.log('   Error details:', error);
    } else {
      console.log('✅ Sign in successful:', data);
    }
  } catch (err) {
    console.error('❌ Sign in error:', err.message);
  }

  // Test 3: Check if user profile exists directly
  console.log('\n3. Testing direct profile access...');
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select('id, email, role_id')
      .eq('email', 'kenwanguka@gmail.com')
      .single();
    
    if (error) {
      console.log('❌ Profile access failed:', error.message);
      console.log('   Error code:', error.code);
      console.log('   Error details:', error.details);
    } else {
      console.log('✅ Profile found:', data);
      
      // Test 4: Check role information
      console.log('\n4. Testing role information...');
      const roleResult = await supabase
        .from('roles')
        .select('*')
        .eq('id', data.role_id)
        .single();
      
      if (roleResult.error) {
        console.log('❌ Role access failed:', roleResult.error.message);
      } else {
        console.log('✅ Role found:', roleResult.data);
      }
    }
  } catch (err) {
    console.error('❌ Profile access error:', err.message);
  }

  console.log('\n=== Debug Complete ===');
}

debugAuthFlow().catch(console.error);
