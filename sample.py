import pandas as pd
import ast

# Load the CSV file
df = pd.read_csv("C:/Users/Sujal Jadhv/Downloads/Chat-Transcript_886d604d-e942-4ca9-8b19-be327ff7941a-1752085800000.csv")

# Container for output
conversations = []

# Group by conversation ID
for chat_id, group in df.groupby("conversation_id"):
    # Get visitor name from first user entry
    user_rows = group[group['actor_type'] == 'f:user']
    if not user_rows.empty:
        first_user = user_rows.iloc[0]
        visitor_name = f"{first_user['actor_first_name']} {first_user['actor_last_name']}".strip()
    else:
        visitor_name = "Unknown Visitor"

    # Remove 'system' and 'bot' messages
    group_filtered = group[~group['actor_type'].isin(['system', 'bot'])].sort_values("created_time")

    # Build conversation text
    conversation_lines = []
    for _, row in group_filtered.iterrows():
        sender = row["actor_type"].replace("f:", "")  # e.g., f:user → user
        try:
            parts = ast.literal_eval(row["message_parts"])
            message = parts[0]["text"]["content"]
        except Exception:
            message = "(Could not parse message)"
        conversation_lines.append(f"{sender}: {message}")

    conversations.append({
        "Chat ID": chat_id,
        "Visitor Name": visitor_name,
        "Conversation": "\n".join(conversation_lines)
    })

# Save to CSV
output_df = pd.DataFrame(conversations)
output_df.to_csv("final_chat_conversations_no_system_no_bot.csv", index=False)

print("✅ Removed system and bot messages. Saved as 'final_chat_conversations_no_system_no_bot.csv'")
