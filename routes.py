from apps import (
    # whatever youd like to list on your routes
)
import volSurfaceUI as volSurfaceUI
from dash.dependencies import Input, Output
from company_styling import favicon_name
from riskapi import runRisk
from flask import request, send_from_directory
import os


def routes(app, server):
    # initialise callbacks for all the pages
    homepage.initialise_callbacks(app)

    # for Risk API
    @server.route("/RiskApi/V1/risk")
    def risk_route():
        portfolio = request.args.get("portfolio", default="*", type=str)
        vol = request.args.get("vol").split(",")
        und = request.args.get("und").split(",")
        level = request.args.get("level", default="high", type=str)
        eval = request.args.get("eval")
        rel = request.args.get("rel", default="abs", type=str)

        # default level back to high
        level = "high"
        ApiInputs = {
            "portfolio": portfolio,
            "vol": vol,
            "und": und,
            "level": level,
            "eval": eval,
            "rel": rel,
        }
        try:
            return runRisk(ApiInputs)
        except Exception as e:
            print("RISK_API: Failed to calculate risk {}".format(str(e)))

    # add icon and title for top of website
    @app.server.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(server.root_path, "assets/images"),
            favicon_name,
            mimetype="image/vnd.microsoft.icon",
        )

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/trades":
            return trades.layout
        else:
            return homepage.layout
