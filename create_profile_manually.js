// Script to manually create a profile for the user
const { createClient } = require('@supabase/supabase-js');

// These would need to be set in your environment
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials not found in environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function createProfileManually() {
  const userId = '289c36cf-8779-4e49-bcfe-b829d0899472';
  const userEmail = 'kenwanguka@gmail.com';
  
  console.log('Creating profile manually for user:', userId);
  
  try {
    const profileData = {
      id: userId,
      email: userEmail,
      full_name: 'Ken Wanguka',
      organization: '',
      role_id: 'ac4c17be-fdb2-4e45-bcc4-96fe27b3be64', // Default user role
      settings: {}
    };

    const { error } = await supabase
      .from('profiles')
      .insert(profileData);

    if (error) {
      console.error('Error creating profile:', error);
    } else {
      console.log('Profile created successfully!');
    }
  } catch (err) {
    console.error('Error in createProfileManually:', err);
  }
}

createProfileManually();
