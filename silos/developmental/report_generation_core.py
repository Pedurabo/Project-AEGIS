#!/usr/bin/env python3
"""
Team 3: Model Training & Deployment - Report Generation System
Developmental Silo: Report templates, automated generation, and export functionality
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import csv
import os
from datetime import datetime
import threading
import webbrowser
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

class AEGISReportGenerator:
    def __init__(self):
        self.name = "AEGIS Report Generator"
        self.version = "1.0.0"
        self.report_templates = {}
        self.generated_reports = {}
        self.report_data = {}
        
        # Initialize report templates
        self.initialize_templates()
        
    def initialize_templates(self):
        """Initialize report templates"""
        self.report_templates = {
            "penetration_test": {
                "title": "AEGIS Penetration Test Report",
                "sections": [
                    "Executive Summary",
                    "Target Information",
                    "Methodology",
                    "Findings",
                    "Vulnerabilities",
                    "Recommendations",
                    "Conclusion"
                ],
                "template": self.penetration_test_template
            },
            "banking_operations": {
                "title": "AEGIS Banking Operations Report",
                "sections": [
                    "Executive Summary",
                    "Operations Overview",
                    "Account Analysis",
                    "Transaction Monitoring",
                    "Security Assessment",
                    "Risk Analysis",
                    "Recommendations"
                ],
                "template": self.banking_operations_template
            },
            "global_dominance": {
                "title": "AEGIS Global Dominance Report",
                "sections": [
                    "Executive Summary",
                    "Dominance Phases",
                    "Control Systems",
                    "Reality Engineering",
                    "Universal Intelligence",
                    "Achievement Metrics",
                    "Future Plans"
                ],
                "template": self.global_dominance_template
            },
            "system_status": {
                "title": "AEGIS System Status Report",
                "sections": [
                    "System Overview",
                    "Component Status",
                    "Performance Metrics",
                    "Operational Status",
                    "Issues and Alerts",
                    "Maintenance Schedule",
                    "Recommendations"
                ],
                "template": self.system_status_template
            },
            "custom": {
                "title": "Custom AEGIS Report",
                "sections": [
                    "Custom Section 1",
                    "Custom Section 2",
                    "Custom Section 3"
                ],
                "template": self.custom_template
            }
        }
    
    def create_report_interface(self, parent):
        """Create report generation interface"""
        report_frame = tk.LabelFrame(
            parent,
            text="📋 REPORT GENERATION SYSTEM",
            font=('Segoe UI', 12, 'bold'),
            fg='#58a6ff',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        report_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.report_notebook = ttk.Notebook(report_frame)
        self.report_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Report creation tab
        self.create_report_creation_tab()
        
        # Templates tab
        self.create_templates_tab()
        
        # Generated reports tab
        self.create_generated_reports_tab()
        
        # Settings tab
        self.create_settings_tab()
    
    def create_report_creation_tab(self):
        """Create report creation tab"""
        creation_frame = tk.Frame(self.report_notebook, bg='#0d1117')
        self.report_notebook.add(creation_frame, text="📝 Create Report")
        
        # Report type selection
        type_frame = tk.LabelFrame(
            creation_frame,
            text="📋 Report Type",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        type_frame.pack(fill='x', padx=10, pady=5)
        
        self.report_type_var = tk.StringVar(value="penetration_test")
        
        for report_type, template_info in self.report_templates.items():
            tk.Radiobutton(
                type_frame,
                text=template_info["title"],
                variable=self.report_type_var,
                value=report_type,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d',
                command=self.update_sections_display
            ).pack(anchor='w', padx=10, pady=2)
        
        # Report details
        details_frame = tk.LabelFrame(
            creation_frame,
            text="📄 Report Details",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        details_frame.pack(fill='x', padx=10, pady=5)
        
        # Title
        title_frame = tk.Frame(details_frame, bg='#0d1117')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            title_frame,
            text="Report Title:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.report_title_var = tk.StringVar()
        title_entry = tk.Entry(
            title_frame,
            textvariable=self.report_title_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        title_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Author
        author_frame = tk.Frame(details_frame, bg='#0d1117')
        author_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            author_frame,
            text="Author:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.report_author_var = tk.StringVar(value="AEGIS System")
        author_entry = tk.Entry(
            author_frame,
            textvariable=self.report_author_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        author_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Sections display
        sections_frame = tk.LabelFrame(
            creation_frame,
            text="📑 Report Sections",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        sections_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Sections listbox
        self.sections_listbox = tk.Listbox(
            sections_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            selectmode='single',
            height=8
        )
        self.sections_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Section content
        content_frame = tk.Frame(sections_frame, bg='#0d1117')
        content_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(
            content_frame,
            text="Section Content:",
            font=('Segoe UI', 9, 'bold'),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(anchor='w')
        
        self.section_content = scrolledtext.ScrolledText(
            content_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            wrap=tk.WORD,
            height=10
        )
        self.section_content.pack(fill='both', expand=True, pady=5)
        
        # Bind section selection
        self.sections_listbox.bind('<<ListboxSelect>>', self.on_section_select)
        
        # Generate button
        generate_btn = tk.Button(
            creation_frame,
            text="Generate Report",
            command=self.generate_report,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        generate_btn.pack(pady=10)
        
        # Initialize sections display
        self.update_sections_display()
    
    def create_templates_tab(self):
        """Create templates tab"""
        templates_frame = tk.Frame(self.report_notebook, bg='#0d1117')
        self.report_notebook.add(templates_frame, text="📋 Templates")
        
        # Templates list
        templates_list_frame = tk.LabelFrame(
            templates_frame,
            text="📋 Available Templates",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        templates_list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Templates treeview
        columns = ('Template', 'Sections', 'Last Modified')
        self.templates_tree = ttk.Treeview(
            templates_list_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        for col in columns:
            self.templates_tree.heading(col, text=col)
            self.templates_tree.column(col, width=150)
        
        self.templates_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate templates
        for template_name, template_info in self.report_templates.items():
            sections_count = len(template_info["sections"])
            self.templates_tree.insert('', 'end', values=(
                template_info["title"],
                f"{sections_count} sections",
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
        
        # Template actions
        actions_frame = tk.Frame(templates_frame, bg='#0d1117')
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        edit_btn = tk.Button(
            actions_frame,
            text="Edit Template",
            command=self.edit_template,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(
            actions_frame,
            text="Delete Template",
            command=self.delete_template,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        delete_btn.pack(side='left', padx=5)
    
    def create_generated_reports_tab(self):
        """Create generated reports tab"""
        reports_frame = tk.Frame(self.report_notebook, bg='#0d1117')
        self.report_notebook.add(reports_frame, text="📄 Generated Reports")
        
        # Reports list
        reports_list_frame = tk.LabelFrame(
            reports_frame,
            text="📄 Generated Reports",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        reports_list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Reports treeview
        columns = ('Title', 'Type', 'Generated', 'Size')
        self.reports_tree = ttk.Treeview(
            reports_list_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        for col in columns:
            self.reports_tree.heading(col, text=col)
            self.reports_tree.column(col, width=150)
        
        self.reports_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Report actions
        actions_frame = tk.Frame(reports_frame, bg='#0d1117')
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        view_btn = tk.Button(
            actions_frame,
            text="View Report",
            command=self.view_report,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        view_btn.pack(side='left', padx=5)
        
        export_btn = tk.Button(
            actions_frame,
            text="Export Report",
            command=self.export_report,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        export_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(
            actions_frame,
            text="Delete Report",
            command=self.delete_report,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        delete_btn.pack(side='left', padx=5)
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = tk.Frame(self.report_notebook, bg='#0d1117')
        self.report_notebook.add(settings_frame, text="⚙️ Settings")
        
        # Export settings
        export_frame = tk.LabelFrame(
            settings_frame,
            text="📤 Export Settings",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        export_frame.pack(fill='x', padx=10, pady=5)
        
        # Default format
        format_frame = tk.Frame(export_frame, bg='#0d1117')
        format_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            format_frame,
            text="Default Export Format:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.default_format_var = tk.StringVar(value="pdf")
        formats = [("PDF", "pdf"), ("HTML", "html"), ("DOCX", "docx"), ("TXT", "txt")]
        
        for text, value in formats:
            tk.Radiobutton(
                format_frame,
                text=text,
                variable=self.default_format_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(side='left', padx=10)
        
        # Auto-save settings
        auto_frame = tk.Frame(export_frame, bg='#0d1117')
        auto_frame.pack(fill='x', padx=10, pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            auto_frame,
            text="Auto-save reports",
            variable=self.auto_save_var,
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117',
            selectcolor='#21262d'
        ).pack(anchor='w')
        
        # Save settings button
        save_btn = tk.Button(
            settings_frame,
            text="Save Settings",
            command=self.save_settings,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        save_btn.pack(pady=10)
    
    def update_sections_display(self):
        """Update sections display based on selected report type"""
        report_type = self.report_type_var.get()
        template_info = self.report_templates[report_type]
        
        # Update title
        self.report_title_var.set(template_info["title"])
        
        # Update sections listbox
        self.sections_listbox.delete(0, tk.END)
        for section in template_info["sections"]:
            self.sections_listbox.insert(tk.END, section)
        
        # Clear content
        self.section_content.delete('1.0', tk.END)
        
        # Store current sections
        self.current_sections = template_info["sections"]
        self.section_data = {section: "" for section in template_info["sections"]}
    
    def on_section_select(self, event):
        """Handle section selection"""
        selection = self.sections_listbox.curselection()
        if selection:
            section_name = self.sections_listbox.get(selection[0])
            
            # Save current content
            if hasattr(self, 'current_section'):
                self.section_data[self.current_section] = self.section_content.get('1.0', tk.END)
            
            # Load new section content
            self.current_section = section_name
            self.section_content.delete('1.0', tk.END)
            self.section_content.insert('1.0', self.section_data.get(section_name, ""))
    
    def generate_report(self):
        """Generate report"""
        report_type = self.report_type_var.get()
        title = self.report_title_var.get()
        author = self.report_author_var.get()
        
        # Save current section content
        if hasattr(self, 'current_section'):
            self.section_data[self.current_section] = self.section_content.get('1.0', tk.END)
        
        # Create report data
        report_data = {
            "type": report_type,
            "title": title,
            "author": author,
            "generated": datetime.now().isoformat(),
            "sections": self.section_data
        }
        
        # Generate report using template
        template_func = self.report_templates[report_type]["template"]
        report_content = template_func(report_data)
        
        # Store generated report
        report_id = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.generated_reports[report_id] = {
            "data": report_data,
            "content": report_content,
            "generated": datetime.now().isoformat()
        }
        
        # Update reports list
        self.update_reports_list()
        
        messagebox.showinfo("Success", f"Report '{title}' generated successfully!")
    
    def penetration_test_template(self, data):
        """Penetration test report template"""
        content = f"""
# {data['title']}

**Generated:** {data['generated']}  
**Author:** {data['author']}

## Executive Summary
{data['sections'].get('Executive Summary', 'Executive summary content goes here.')}

## Target Information
{data['sections'].get('Target Information', 'Target information content goes here.')}

## Methodology
{data['sections'].get('Methodology', 'Methodology content goes here.')}

## Findings
{data['sections'].get('Findings', 'Findings content goes here.')}

## Vulnerabilities
{data['sections'].get('Vulnerabilities', 'Vulnerabilities content goes here.')}

## Recommendations
{data['sections'].get('Recommendations', 'Recommendations content goes here.')}

## Conclusion
{data['sections'].get('Conclusion', 'Conclusion content goes here.')}
"""
        return content
    
    def banking_operations_template(self, data):
        """Banking operations report template"""
        content = f"""
# {data['title']}

**Generated:** {data['generated']}  
**Author:** {data['author']}

## Executive Summary
{data['sections'].get('Executive Summary', 'Executive summary content goes here.')}

## Operations Overview
{data['sections'].get('Operations Overview', 'Operations overview content goes here.')}

## Account Analysis
{data['sections'].get('Account Analysis', 'Account analysis content goes here.')}

## Transaction Monitoring
{data['sections'].get('Transaction Monitoring', 'Transaction monitoring content goes here.')}

## Security Assessment
{data['sections'].get('Security Assessment', 'Security assessment content goes here.')}

## Risk Analysis
{data['sections'].get('Risk Analysis', 'Risk analysis content goes here.')}

## Recommendations
{data['sections'].get('Recommendations', 'Recommendations content goes here.')}
"""
        return content
    
    def global_dominance_template(self, data):
        """Global dominance report template"""
        content = f"""
# {data['title']}

**Generated:** {data['generated']}  
**Author:** {data['author']}

## Executive Summary
{data['sections'].get('Executive Summary', 'Executive summary content goes here.')}

## Dominance Phases
{data['sections'].get('Dominance Phases', 'Dominance phases content goes here.')}

## Control Systems
{data['sections'].get('Control Systems', 'Control systems content goes here.')}

## Reality Engineering
{data['sections'].get('Reality Engineering', 'Reality engineering content goes here.')}

## Universal Intelligence
{data['sections'].get('Universal Intelligence', 'Universal intelligence content goes here.')}

## Achievement Metrics
{data['sections'].get('Achievement Metrics', 'Achievement metrics content goes here.')}

## Future Plans
{data['sections'].get('Future Plans', 'Future plans content goes here.')}
"""
        return content
    
    def system_status_template(self, data):
        """System status report template"""
        content = f"""
# {data['title']}

**Generated:** {data['generated']}  
**Author:** {data['author']}

## System Overview
{data['sections'].get('System Overview', 'System overview content goes here.')}

## Component Status
{data['sections'].get('Component Status', 'Component status content goes here.')}

## Performance Metrics
{data['sections'].get('Performance Metrics', 'Performance metrics content goes here.')}

## Operational Status
{data['sections'].get('Operational Status', 'Operational status content goes here.')}

## Issues and Alerts
{data['sections'].get('Issues and Alerts', 'Issues and alerts content goes here.')}

## Maintenance Schedule
{data['sections'].get('Maintenance Schedule', 'Maintenance schedule content goes here.')}

## Recommendations
{data['sections'].get('Recommendations', 'Recommendations content goes here.')}
"""
        return content
    
    def custom_template(self, data):
        """Custom report template"""
        content = f"""
# {data['title']}

**Generated:** {data['generated']}  
**Author:** {data['author']}

"""
        for section_name, section_content in data['sections'].items():
            content += f"## {section_name}\n{section_content}\n\n"
        
        return content
    
    def update_reports_list(self):
        """Update generated reports list"""
        # Clear existing items
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        
        # Add reports
        for report_id, report_info in self.generated_reports.items():
            title = report_info['data']['title']
            report_type = report_info['data']['type']
            generated = report_info['generated']
            size = len(str(report_info['content']))
            
            self.reports_tree.insert('', 'end', values=(
                title,
                report_type,
                generated,
                f"{size} chars"
            ))
    
    def edit_template(self):
        """Edit template"""
        messagebox.showinfo("Info", "Template editing feature coming soon!")
    
    def delete_template(self):
        """Delete template"""
        messagebox.showinfo("Info", "Template deletion feature coming soon!")
    
    def view_report(self):
        """View report"""
        selection = self.reports_tree.selection()
        if selection:
            item = self.reports_tree.item(selection[0])
            title = item['values'][0]
            
            # Find report
            for report_id, report_info in self.generated_reports.items():
                if report_info['data']['title'] == title:
                    self.show_report_viewer(report_info['content'], title)
                    break
    
    def show_report_viewer(self, content, title):
        """Show report viewer"""
        viewer_window = tk.Toplevel()
        viewer_window.title(f"Report Viewer - {title}")
        viewer_window.geometry("800x600")
        viewer_window.configure(bg='#0d1117')
        
        # Content display
        content_text = scrolledtext.ScrolledText(
            viewer_window,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        content_text.pack(fill='both', expand=True, padx=10, pady=10)
        content_text.insert('1.0', content)
    
    def export_report(self):
        """Export report"""
        selection = self.reports_tree.selection()
        if selection:
            item = self.reports_tree.item(selection[0])
            title = item['values'][0]
            
            # Find report
            for report_id, report_info in self.generated_reports.items():
                if report_info['data']['title'] == title:
                    self.export_report_file(report_info, title)
                    break
    
    def export_report_file(self, report_info, title):
        """Export report to file"""
        file_path = filedialog.asksaveasfilename(
            title="Export Report",
            defaultextension=f".{self.default_format_var.get()}",
            initialvalue=f"{title}.{self.default_format_var.get()}",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("HTML files", "*.html"),
                ("Text files", "*.txt")
            ]
        )
        
        if file_path:
            try:
                export_format = self.default_format_var.get()
                
                if export_format == "pdf":
                    self.export_to_pdf(report_info['content'], file_path)
                elif export_format == "html":
                    self.export_to_html(report_info['content'], file_path)
                else:
                    with open(file_path, 'w') as f:
                        f.write(report_info['content'])
                
                messagebox.showinfo("Success", f"Report exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_to_pdf(self, content, file_path):
        """Export to PDF"""
        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            story = []
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30
            )
            
            # Split content into lines
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('# '):
                    # Main title
                    title = line[2:]
                    story.append(Paragraph(title, title_style))
                    story.append(Spacer(1, 12))
                elif line.startswith('## '):
                    # Section title
                    section = line[3:]
                    story.append(Paragraph(section, styles['Heading2']))
                    story.append(Spacer(1, 12))
                elif line.startswith('**') and line.endswith('**'):
                    # Bold text
                    bold_text = line[2:-2]
                    story.append(Paragraph(bold_text, styles['Normal']))
                    story.append(Spacer(1, 6))
                elif line:
                    # Regular text
                    story.append(Paragraph(line, styles['Normal']))
                    story.append(Spacer(1, 6))
            
            doc.build(story)
            
        except Exception as e:
            # Fallback to text export
            with open(file_path, 'w') as f:
                f.write(content)
    
    def export_to_html(self, content, file_path):
        """Export to HTML"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AEGIS Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #58a6ff; }}
        h2 {{ color: #4ecdc4; }}
        .metadata {{ color: #666; font-style: italic; }}
    </style>
</head>
<body>
"""
        
        # Convert markdown to HTML
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                html_content += f"<h1>{line[2:]}</h1>\n"
            elif line.startswith('## '):
                html_content += f"<h2>{line[3:]}</h2>\n"
            elif line.startswith('**') and line.endswith('**'):
                html_content += f"<p class='metadata'>{line[2:-2]}</p>\n"
            elif line:
                html_content += f"<p>{line}</p>\n"
        
        html_content += """
</body>
</html>
"""
        
        with open(file_path, 'w') as f:
            f.write(html_content)
    
    def delete_report(self):
        """Delete report"""
        selection = self.reports_tree.selection()
        if selection:
            item = self.reports_tree.item(selection[0])
            title = item['values'][0]
            
            if messagebox.askyesno("Confirm", f"Delete report '{title}'?"):
                # Find and remove report
                for report_id, report_info in list(self.generated_reports.items()):
                    if report_info['data']['title'] == title:
                        del self.generated_reports[report_id]
                        break
                
                self.update_reports_list()
    
    def save_settings(self):
        """Save settings"""
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def get_generated_reports(self):
        """Get generated reports"""
        return self.generated_reports 