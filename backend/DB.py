from supabase.client import create_client 

supabaseUrl = ""
supabaseKey = ""

# Create Supabase client
database = create_client(supabaseUrl,supabaseKey)
