import { createClient } from '@supabase/supabase-js';

// Directly use the service role key (for testing only)
const supabase = createClient(
  'https://gagcprlttjerhciicwzb.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdhZ2Nwcmx0dGplcmhjaWljd3piIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5OTIwNSwiZXhwIjoyMDY2Nzc1MjA1fQ.qnyiIfnYKnO8hh820QeO4f7mM3SBQVqMF8R4H7cUIxI'
);

const usersToReset = [
  'john.smith@company.com',
  'kenwanguka@gmail.com', 
  'sarah.johnson@company.com',
  'mike.chen@company.com'
];

const resetPassword = async () => {
  for (const email of usersToReset) {
    const { data: users, error: listError } = await supabase.auth.admin.listUsers({ email });
    if (listError || !users?.users?.length) {
      console.error(`Failed to find user ${email}:`, listError?.message);
      continue;
    }
    const user = users.users[0];

    const { error: updateError } = await supabase.auth.admin.updateUserById(user.id, {
      password: 'password'
    });

    if (updateError) {
      console.error(`Failed to reset password for ${email}:`, updateError.message);
    } else {
      console.log(`Password reset for ${email}`);
    }
  }
};

resetPassword();
