"""
Enterprise Product Analytics Platform
Dashboard Service Layer
"""

from loguru import logger

from src.dashboard_engine.dashboard_data import DashboardData


class DashboardService:

    def __init__(self):
        self.data = DashboardData()

    def get_dashboard(self):

        logger.info("Loading dashboard data")

        dashboard = {
            "kpis": self.data.kpis(),
            "event_summary": self.data.event_summary(),
            "daily_activity": self.data.daily_activity(),
        }

        logger.success("Dashboard data loaded successfully")

        return dashboard

    def print_dashboard(self):

        dashboard = self.get_dashboard()

        print("=" * 80)
        print("EXECUTIVE DASHBOARD")
        print("=" * 80)

        print("\nKPIs")
        print(dashboard["kpis"].to_string(index=False))

        print("\nEVENT SUMMARY")
        print(dashboard["event_summary"].to_string(index=False))

        print("\nDAILY ACTIVITY")
        print(dashboard["daily_activity"].head(10).to_string(index=False))

        self.data.close()


if __name__ == "__main__":
    DashboardService().print_dashboard()