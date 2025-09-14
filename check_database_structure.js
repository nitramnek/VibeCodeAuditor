// Simple script to check database structure
const { createClient } = require('@supabase/supabase-js');

// These would need to be set in your environment
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found in environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function checkDatabaseStructure() {
  console.log('Checking database structure...');
  
  try {
    // Check if profiles table exists and get its structure
    const { data: tableInfo, error } = await supabase
      .from('information_schema.columns')
      .select('column_name, data_type, is_nullable')
      .eq('table_name', 'profiles')
      .eq('table_schema', 'public');
    
    if (error) {
      console.error('Error checking table structure:', error);
      return;
    }
    
    console.log('Profiles table columns:');
    tableInfo.forEach(col => {
      console.log(`  ${col.column_name}: ${col.data_type} ${col.is_nullable === 'YES' ? 'NULL' : 'NOT NULL'}`);
    });
    
    // Try a simple query to see what happens
    console.log('\nTrying simple query...');
    const { data: simpleData, error: simpleError } = await supabase
      .from('profiles')
      .select('id, email')
      .limit(1);
    
    if (simpleError) {
      console.error('Simple query error:', simpleError);
    } else {
      console.log('Simple query result:', simpleData);
    }
    
  } catch (err) {
    console.error('Error in checkDatabaseStructure:', err);
  }
}

checkDatabaseStructure();
