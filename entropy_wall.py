#!/usr/bin/env python3
"""
Wall of Entropy - Public Transparency Log

A transparent, public ledger of unauthorized or unethical access attempts.
All violations are logged and made publicly viewable for maximum transparency.

Operating under Lex Amoris - Transparency First - Public Accountability
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import sys


class EntropyWall:
    """
    Main Wall of Entropy logging and visualization system.
    
    Provides:
    - Transparent logging of security events
    - Public queryable interface
    - Statistical analysis
    - Dashboard data generation
    """
    
    def __init__(self, data_dir: str = ".entropy_wall"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.events_log = self.data_dir / "events.log"
        self.summary_file = self.data_dir / "summary.json"
        self.dashboard_data = self.data_dir / "dashboard.json"
    
    def log_event(self, 
                  violation_type: str,
                  source_identifier: str,
                  action_taken: str,
                  severity: str,
                  details: Optional[Dict] = None) -> Dict:
        """
        Log a security event to the Wall of Entropy.
        
        Args:
            violation_type: Type of violation (NSR_BREACH, OLF_VIOLATION, etc.)
            source_identifier: Hashed identifier of source
            action_taken: Action taken (BLOCKED, QUARANTINED, etc.)
            severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
            details: Optional additional details
            
        Returns:
            The logged event
        """
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "violation_type": violation_type,
            "source_identifier": source_identifier,
            "action_taken": action_taken,
            "severity": severity,
            "details": details or {}
        }
        
        # Append to events log
        try:
            with open(self.events_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            print(f"Error logging event: {e}", file=sys.stderr)
        
        # Update summary
        self._update_summary()
        
        # Regenerate dashboard data
        self._generate_dashboard_data()
        
        return event
    
    def get_recent_events(self, count: int = 50) -> List[Dict]:
        """Get the most recent events."""
        if not self.events_log.exists():
            return []
        
        events = []
        try:
            with open(self.events_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines[-count:]:
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            print(f"Error reading events: {e}", file=sys.stderr)
        
        return events
    
    def query_events(self,
                    violation_type: Optional[str] = None,
                    severity: Optional[str] = None,
                    since: Optional[str] = None,
                    until: Optional[str] = None,
                    action: Optional[str] = None) -> List[Dict]:
        """
        Query events with filters.
        
        Args:
            violation_type: Filter by violation type
            severity: Filter by severity level
            since: ISO timestamp - events after this time
            until: ISO timestamp - events before this time
            action: Filter by action taken
            
        Returns:
            Filtered list of events
        """
        if not self.events_log.exists():
            return []
        
        events = []
        try:
            with open(self.events_log, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        
                        # Apply filters
                        if violation_type and event.get("violation_type") != violation_type:
                            continue
                        
                        if severity and event.get("severity") != severity:
                            continue
                        
                        if action and event.get("action_taken") != action:
                            continue
                        
                        event_time = event.get("timestamp", "")
                        if since and event_time < since:
                            continue
                        
                        if until and event_time > until:
                            continue
                        
                        events.append(event)
                        
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Error querying events: {e}", file=sys.stderr)
        
        return events
    
    def get_statistics(self, time_period: Optional[str] = None) -> Dict:
        """
        Generate statistics about logged events.
        
        Args:
            time_period: Optional time period ('24h', '7d', '30d', 'all')
            
        Returns:
            Statistical summary
        """
        # Determine time filter
        since = None
        if time_period:
            now = datetime.utcnow()
            if time_period == '24h':
                since = (now - timedelta(hours=24)).isoformat() + "Z"
            elif time_period == '7d':
                since = (now - timedelta(days=7)).isoformat() + "Z"
            elif time_period == '30d':
                since = (now - timedelta(days=30)).isoformat() + "Z"
        
        # Get events
        events = self.query_events(since=since) if since else self.get_all_events()
        
        # Calculate statistics
        stats = {
            "time_period": time_period or "all",
            "total_events": len(events),
            "by_violation_type": {},
            "by_severity": {},
            "by_action": {},
            "unique_sources": set(),
            "timeline": []
        }
        
        for event in events:
            # Count by violation type
            vtype = event.get("violation_type", "UNKNOWN")
            stats["by_violation_type"][vtype] = stats["by_violation_type"].get(vtype, 0) + 1
            
            # Count by severity
            severity = event.get("severity", "UNKNOWN")
            stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
            
            # Count by action
            action = event.get("action_taken", "UNKNOWN")
            stats["by_action"][action] = stats["by_action"].get(action, 0) + 1
            
            # Track unique sources
            source = event.get("source_identifier")
            if source:
                stats["unique_sources"].add(source)
        
        # Convert set to count
        stats["unique_sources_count"] = len(stats["unique_sources"])
        del stats["unique_sources"]
        
        return stats
    
    def get_all_events(self) -> List[Dict]:
        """Get all events from the log."""
        if not self.events_log.exists():
            return []
        
        events = []
        try:
            with open(self.events_log, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        events.append(event)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Error reading all events: {e}", file=sys.stderr)
        
        return events
    
    def _update_summary(self):
        """Update the summary file with latest statistics."""
        stats = self.get_statistics("all")
        
        summary = {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "statistics": {
                "all_time": stats,
                "last_24h": self.get_statistics("24h"),
                "last_7d": self.get_statistics("7d"),
                "last_30d": self.get_statistics("30d")
            }
        }
        
        try:
            with open(self.summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
        except Exception as e:
            print(f"Error updating summary: {e}", file=sys.stderr)
    
    def _generate_dashboard_data(self):
        """Generate data file for dashboard visualization."""
        recent_events = self.get_recent_events(100)
        stats = self.get_statistics("all")
        
        dashboard = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "status": "ACTIVE",
            "recent_events": recent_events[-10:],  # Last 10 for dashboard
            "statistics": {
                "total_events": stats["total_events"],
                "by_violation_type": stats["by_violation_type"],
                "by_severity": stats["by_severity"],
                "unique_sources": stats["unique_sources_count"]
            },
            "threat_level": self._calculate_threat_level(stats)
        }
        
        try:
            with open(self.dashboard_data, 'w', encoding='utf-8') as f:
                json.dump(dashboard, f, indent=2)
        except Exception as e:
            print(f"Error generating dashboard data: {e}", file=sys.stderr)
    
    def _calculate_threat_level(self, stats: Dict) -> str:
        """Calculate overall threat level from statistics."""
        total = stats["total_events"]
        
        # Check recent activity (last 24h)
        recent_stats = self.get_statistics("24h")
        recent_total = recent_stats["total_events"]
        
        # Count critical/high severity
        critical = stats["by_severity"].get("CRITICAL", 0)
        high = stats["by_severity"].get("HIGH", 0)
        
        if critical > 0 or recent_total > 10:
            return "RED"
        elif high > 2 or recent_total > 5:
            return "ORANGE"
        elif high > 0 or recent_total > 0:
            return "YELLOW"
        else:
            return "GREEN"
    
    def export_html_report(self, output_file: str = "entropy_wall_report.html"):
        """
        Export a standalone HTML report of the Wall of Entropy.
        
        Args:
            output_file: Path to output HTML file
        """
        stats = self.get_statistics("all")
        recent_events = self.get_recent_events(50)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wall of Entropy - Public Security Log</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #00d9ff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #aaa;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .stat-card h3 {{
            margin-top: 0;
            color: #00d9ff;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #fff;
        }}
        .events-table {{
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: rgba(0, 217, 255, 0.2);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #00d9ff;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        tr:hover {{
            background: rgba(255, 255, 255, 0.05);
        }}
        .severity-CRITICAL {{ color: #ff4757; font-weight: bold; }}
        .severity-HIGH {{ color: #ff6348; }}
        .severity-MEDIUM {{ color: #ffa502; }}
        .severity-LOW {{ color: #f1c40f; }}
        .threat-level {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .threat-GREEN {{ background: #27ae60; color: white; }}
        .threat-YELLOW {{ background: #f1c40f; color: black; }}
        .threat-ORANGE {{ background: #e67e22; color: white; }}
        .threat-RED {{ background: #e74c3c; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏛️ Wall of Entropy</h1>
        <p class="subtitle">Public Transparency Log - Internet Organica</p>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total Events</h3>
                <div class="stat-value">{stats['total_events']}</div>
            </div>
            <div class="stat-card">
                <h3>Unique Sources</h3>
                <div class="stat-value">{stats['unique_sources_count']}</div>
            </div>
            <div class="stat-card">
                <h3>Threat Level</h3>
                <div class="stat-value">
                    <span class="threat-level threat-{self._calculate_threat_level(stats)}">
                        {self._calculate_threat_level(stats)}
                    </span>
                </div>
            </div>
        </div>
        
        <div class="events-table">
            <h2 style="padding: 20px 20px 0 20px; color: #00d9ff;">Recent Events</h2>
            <table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Violation Type</th>
                        <th>Severity</th>
                        <th>Action Taken</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for event in reversed(recent_events[-30:]):
            timestamp = event.get("timestamp", "")[:19].replace("T", " ")
            violation = event.get("violation_type", "UNKNOWN")
            severity = event.get("severity", "")
            action = event.get("action_taken", "")
            
            html += f"""
                    <tr>
                        <td>{timestamp}</td>
                        <td>{violation}</td>
                        <td class="severity-{severity}">{severity}</td>
                        <td>{action}</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <p style="text-align: center; margin-top: 40px; color: #888;">
            Generated: """ + datetime.utcnow().isoformat()[:19] + """ UTC<br>
            <em>Operating under Lex Amoris - Transparency First - Public Accountability</em>
        </p>
    </div>
</body>
</html>
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✓ HTML report generated: {output_file}")
        except Exception as e:
            print(f"Error exporting HTML report: {e}", file=sys.stderr)


def main():
    """CLI interface for Wall of Entropy."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Wall of Entropy - Public Transparency Log'
    )
    parser.add_argument(
        '--recent',
        type=int,
        metavar='N',
        help='Show N most recent events (default: 10)'
    )
    parser.add_argument(
        '--query',
        type=str,
        metavar='FILTER',
        help='Query events (e.g., "violation_type=NSR_BREACH")'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics'
    )
    parser.add_argument(
        '--period',
        type=str,
        choices=['24h', '7d', '30d', 'all'],
        default='all',
        help='Time period for statistics'
    )
    parser.add_argument(
        '--export-html',
        type=str,
        metavar='FILE',
        help='Export HTML report to file'
    )
    
    args = parser.parse_args()
    
    wall = EntropyWall()
    
    if args.recent:
        events = wall.get_recent_events(args.recent)
        print(f"\n📊 {len(events)} Most Recent Events")
        print("=" * 80)
        
        for event in events:
            timestamp = event.get("timestamp", "")[:19]
            violation = event.get("violation_type", "UNKNOWN")
            severity = event.get("severity", "")
            action = event.get("action_taken", "")
            
            print(f"{timestamp} | {severity:8s} | {violation:20s} | {action}")
        
        print("=" * 80)
    
    elif args.query:
        # Parse query
        parts = args.query.split("=")
        if len(parts) != 2:
            print("Query format: key=value")
            return
        
        key, value = parts
        
        if key == "violation_type":
            events = wall.query_events(violation_type=value)
        elif key == "severity":
            events = wall.query_events(severity=value)
        elif key == "action":
            events = wall.query_events(action=value)
        else:
            print(f"Unknown query key: {key}")
            return
        
        print(f"\n📊 Query Results: {len(events)} events")
        print("=" * 80)
        
        for event in events:
            print(json.dumps(event, indent=2))
            print("-" * 80)
    
    elif args.stats:
        stats = wall.get_statistics(args.period)
        
        print(f"\n📊 Wall of Entropy Statistics ({args.period})")
        print("=" * 80)
        print(json.dumps(stats, indent=2))
        print("=" * 80)
    
    elif args.export_html:
        wall.export_html_report(args.export_html)
    
    else:
        # Default: show summary
        recent = wall.get_recent_events(10)
        stats = wall.get_statistics("all")
        
        print("\n🏛️  Wall of Entropy - Public Transparency Log")
        print("=" * 80)
        print(f"Total Events: {stats['total_events']}")
        print(f"Unique Sources: {stats['unique_sources_count']}")
        print(f"Threat Level: {wall._calculate_threat_level(stats)}")
        print("\nRecent Events:")
        
        for event in recent[-5:]:
            timestamp = event.get("timestamp", "")[:19]
            violation = event.get("violation_type", "UNKNOWN")
            print(f"  • {timestamp} - {violation}")
        
        print("\nUse --help for more options")
        print("=" * 80)


if __name__ == "__main__":
    main()
