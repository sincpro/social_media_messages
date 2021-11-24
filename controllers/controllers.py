# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.http import Response
import logging


_logger = logging.getLogger(__name__)


class ControllerWebhookMessenger(http.Controller):
    @http.route(
        "/webhook_messenger", methods=["POST"], type="json", auth="public", csrf=False
    )
    def webhook(self, **kw):
        data = request.jsonrequest
        _logger.info(data)
        if data["object"] == "page":
            social_network_identifier = http.request.env[
                "social.metwork.identifier"
            ].sudo()
            try:
                social_network_identifier.identifier("Facebook", data=data)
            except:
                pass
            return "EVENT_RECEIVED"
        else:
            return Response(status=404)

    @http.route("/webhook_messenger", methods=["GET"], auth="public")
    def verificacion_webhook(self, **kw):
        VERIFY_TOKEN = "Hola_mundo"

        data = request
        mode = data.params["hub.mode"]
        token = data.params["hub.verify_token"]
        challenge = data.params["hub.challenge"]

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                _logger.info("WEBHOOK_VERIFIED")
                return challenge
            else:
                return Response(status=403)
