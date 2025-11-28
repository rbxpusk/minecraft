"""Crash Report Analyzer - Diagnose server crashes"""

class CrashAnalyzer:
    def __init__(self, ssh):
        self.ssh = ssh
        self.mc_dir = "~/minecraft"
    
    def get_latest_crash(self):
        """Get the latest crash report"""
        try:
            # Find latest crash report with timestamp
            output, _ = self.ssh.execute(
                f"ls -lt {self.mc_dir}/crash-reports/*.txt 2>/dev/null | head -5"
            )
            
            if not output.strip():
                return None, "No crash reports found", None
            
            # Get the most recent file
            crash_file_output, _ = self.ssh.execute(
                f"ls -t {self.mc_dir}/crash-reports/*.txt 2>/dev/null | head -1"
            )
            
            crash_file = crash_file_output.strip()
            
            # Get file timestamp
            timestamp, _ = self.ssh.execute(
                f"stat -c '%y' {crash_file} 2>/dev/null || stat -f '%Sm' {crash_file}"
            )
            
            # Read crash report
            content, _ = self.ssh.execute(f"cat {crash_file}")
            
            return crash_file, content, timestamp.strip()
        except Exception as e:
            return None, str(e), None
    
    def list_recent_crashes(self):
        """List recent crash reports"""
        try:
            output, _ = self.ssh.execute(
                f"ls -lth {self.mc_dir}/crash-reports/*.txt 2>/dev/null | head -10"
            )
            return output
        except:
            return "Could not list crash reports"
    
    def analyze_crash(self, crash_content):
        """Analyze crash report and provide diagnosis"""
        if not crash_content:
            return "No crash data to analyze"
        
        issues = []
        solutions = []
        
        # Check for common issues
        if "java.lang.OutOfMemoryError" in crash_content:
            issues.append("❌ OUT OF MEMORY")
            solutions.append("• Increase server RAM (add more -Xmx in start script)")
            solutions.append("• Remove some mods to reduce memory usage")
            solutions.append("• Use Java 8 or 11 instead of Java 21 for 1.16.5")
        
        if "Unsupported Java detected" in crash_content or "Java 21" in crash_content:
            issues.append("❌ INCOMPATIBLE JAVA VERSION")
            solutions.append("• Forge 1.16.5 requires Java 8 or Java 11")
            solutions.append("• Java 21 is too new for this version")
            solutions.append("• Install Java 11: apt install openjdk-11-jdk")
            solutions.append("• Update start script to use Java 11")
        
        if "ClassNotFoundException" in crash_content or "NoClassDefFoundError" in crash_content:
            issues.append("❌ MISSING MOD DEPENDENCY")
            solutions.append("• A mod is missing required dependencies")
            solutions.append("• Check which mod is mentioned in the error")
            solutions.append("• Install missing dependency mods")
        
        if "Mixin" in crash_content and "failed" in crash_content.lower():
            issues.append("❌ MOD COMPATIBILITY ISSUE")
            solutions.append("• Mods are conflicting with each other")
            solutions.append("• Try removing recently added mods")
            solutions.append("• Check mod versions match your Minecraft version")
        
        if "DuplicateModsFoundException" in crash_content:
            issues.append("❌ DUPLICATE MODS")
            solutions.append("• You have the same mod installed twice")
            solutions.append("• Check mods folder for duplicates")
            solutions.append("• Remove older versions")
        
        if "Dynmap" in crash_content and "error" in crash_content.lower():
            issues.append("⚠️ DYNMAP ERROR")
            solutions.append("• Dynmap may be incompatible with your Forge version")
            solutions.append("• Try a different Dynmap version")
            solutions.append("• Check if Dynmap supports Forge 1.16.5")
        
        # Extract key error lines
        error_lines = []
        for line in crash_content.split('\n'):
            if any(keyword in line for keyword in ['Exception', 'Error', 'Caused by', 'at ']):
                error_lines.append(line.strip())
                if len(error_lines) >= 10:
                    break
        
        # Build diagnosis
        diagnosis = "🔍 CRASH ANALYSIS\n\n"
        
        if issues:
            diagnosis += "DETECTED ISSUES:\n"
            for issue in issues:
                diagnosis += f"{issue}\n"
            diagnosis += "\n"
        
        if solutions:
            diagnosis += "RECOMMENDED SOLUTIONS:\n"
            for i, solution in enumerate(solutions, 1):
                diagnosis += f"{i}. {solution}\n"
            diagnosis += "\n"
        
        if error_lines:
            diagnosis += "KEY ERROR LINES:\n"
            diagnosis += "\n".join(error_lines[:10])
            diagnosis += "\n"
        
        if not issues:
            diagnosis += "⚠️ Could not auto-diagnose the issue.\n"
            diagnosis += "Check the full crash report for details.\n"
        
        return diagnosis
    
    def get_java_version(self):
        """Get current Java version"""
        try:
            output, _ = self.ssh.execute("java -version 2>&1 | head -1")
            return output.strip()
        except:
            return "Unknown"
    
    def check_mod_conflicts(self):
        """Check for duplicate or conflicting mods"""
        try:
            # Find duplicate mod names
            output, _ = self.ssh.execute(
                f"cd {self.mc_dir}/mods && ls *.jar | sed 's/-[0-9].*//' | sort | uniq -d"
            )
            
            if output.strip():
                return f"Potential duplicates found:\n{output}"
            else:
                return "No obvious duplicates detected"
        except:
            return "Could not check for conflicts"
