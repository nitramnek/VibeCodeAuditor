// Simple test to check if Node.js is working
console.log('=== Simple Test ===');
console.log('Node.js version:', process.version);
console.log('Current directory:', process.cwd());
console.log('Environment variables:');
console.log('  SUPABASE_URL:', process.env.REACT_APP_SUPABASE_URL ? '*** (set)' : 'Not set');
console.log('  SUPABASE_ANON_KEY:', process.env.REACT_APP_SUPABASE_ANON_KEY ? '*** (set)' : 'Not set');
console.log('=== Test Complete ===');
