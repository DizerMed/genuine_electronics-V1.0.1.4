with open('src/components/AdminPortal.tsx', 'r') as f:
    content = f.read()

# Extract the block
start_idx = content.find("{/* New Order Notification Alert */}")
end_idx = content.find("</AnimatePresence>", start_idx) + len("</AnimatePresence>")

if start_idx != -1 and end_idx != -1:
    block = content[start_idx:end_idx]
    
    # Remove it
    content = content[:start_idx] + content[end_idx:]
    
    # Find the end of AdminPortal.
    # AdminPortal ends with:
    #       </main>
    #     </div>
    #   );
    # };
    # Let's search for `      </main>\n    </div>\n  );\n};` or similar.
    # Actually, it's easier to search for `<AnimatePresence>\n          {toasts.map((toast) => (` inside AdminPortal.
    # Let's just insert it right before the last closing tags of AdminPortal.
    # I'll just append it before `      </main>`
    
    main_end_idx = content.rfind("</main>")
    if main_end_idx != -1:
        content = content[:main_end_idx] + block + "\n" + content[main_end_idx:]
        
    with open('src/components/AdminPortal.tsx', 'w') as f:
        f.write(content)
        
    print("Fixed AdminPortal.")
else:
    print("Block not found!")
