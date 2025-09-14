// Test profile fetching to verify the 406 error is fixed
const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found.');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testProfileFetch() {
  console.log('=== Testing Profile Fetch ===');
  
  const userId = '289c36cf-8779-4e49-bcfe-b829d0899472';
  
  try {
    // Test the exact query that was failing
    console.log('\n1. Testing profile fetch with join...');
    const { data, error } = await supabase
      .from('profiles')
      .select(`
        id,
        email,
        role_id,
        roles (name, description)
      `)
      .eq('id', userId)
      .single();

    if (error) {
      console.error('❌ Error with join:', error.message);
      console.log('Error code:', error.code);
      
      // Test without join
      console.log('\n2. Testing profile fetch without join...');
      const { data: simpleData, error: simpleError } = await supabase
        .from('profiles')
        .select(`
          id,
          email,
          role_id
        `)
        .eq('id', userId)
        .single();

      if (simpleError) {
        console.error('❌ Error without join:', simpleError.message);
        console.log('Error code:', simpleError.code);
      } else {
        console.log('✅ Success without join:', simpleData);
      }
    } else {
      console.log('✅ Success with join:', data);
    }
    
  } catch (err) {
    console.error('❌ Unexpected error:', err.message);
  }
  
  console.log('\n=== Test Complete ===');
}

testProfileFetch().catch(console.error);
