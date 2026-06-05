def fix_closing_divs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_end_in = '''<li class="flex gap-4 text-sm leading-relaxed" style="color:var(--secondary);"><span style="color:#1A1A1E; font-weight:300;">—</span><span><strong class="text-primary font-medium">Finition vitres</strong> — dégraissage haute clarté, sans trace.</span></li>
                </ul>
            </div>'''
            
    new_end_in = '''<li class="flex gap-4 text-sm leading-relaxed" style="color:var(--secondary);"><span style="color:#1A1A1E; font-weight:300;">—</span><span><strong class="text-primary font-medium">Finition vitres</strong> — dégraissage haute clarté, sans trace.</span></li>
                </ul>
            </div>
            </div>'''

    old_end_ex = '''<li class="flex gap-4 text-sm leading-relaxed" style="color:var(--secondary);"><span style="color:#1A1A1E; font-weight:300;">—</span><span><strong class="text-primary font-medium">Dressing pneus</strong> — effet noir satiné durable.</span></li>
                </ul>
            </div>'''
            
    new_end_ex = '''<li class="flex gap-4 text-sm leading-relaxed" style="color:var(--secondary);"><span style="color:#1A1A1E; font-weight:300;">—</span><span><strong class="text-primary font-medium">Dressing pneus</strong> — effet noir satiné durable.</span></li>
                </ul>
            </div>
            </div>'''

    content = content.replace(old_end_in, new_end_in)
    content = content.replace(old_end_ex, new_end_ex)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_closing_divs('index.html')
