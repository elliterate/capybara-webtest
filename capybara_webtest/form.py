import os
import re
from webtest import Upload
from xpath import dsl as x
from xpath.renderer import to_xpath

from capybara_webtest.node import Node


class Form(Node):
    def params(self, button):
        params = []

        types = ["input", "select", "textarea"]
        xpath = x.descendant(*types)[~x.attr("form")]
        if self.native.get("id"):
            xpath += x.anywhere(*types)[x.attr("form") == self.native.get("id")]
        xpath = xpath[~x.attr("disabled")]

        for field in self._find_xpath(to_xpath(xpath)):
            if field.tag_name == "input":
                if field["type"] in ["checkbox", "radio"]:
                    if field.checked:
                        params.append((field["name"], field.value))
                elif field["type"] == "file":
                    if self._multipart:
                        if field.value:
                            params.append(
                                (field["name"], Upload(os.path.basename(field.value), content=open(field.value, "rb").read())))
                        # else:
                        #     # TODO: Fix this?
                        #     params.append((field["name"], Upload(content_type="application/octet-stream")))
                    else:
                        if field.value:
                            params.append((field["name"], os.path.basename(field.value)))
                elif field["type"] in ["submit", "reset", "image"]:
                    pass
                else:
                    params.append((field["name"], field.value))
            elif field.tag_name == "textarea":
                if field.value:
                    params.append((field["name"], re.sub("\n", "\r\n", field.value)))
            elif field.tag_name == "select":
                if field["multiple"] == "multiple":
                    options = field.native.xpath(".//option[@selected='selected']")
                    for option in options:
                        params.append((field["name"], option.get("value", option.text)))
                else:
                    options = field.native.xpath(".//option[@selected='selected']")
                    if not len(options):
                        options = field.native.xpath(".//option")
                    if len(options):
                        params.append((field["name"], options[0].get("value", options[0].text)))

        params.append((button["name"], button["value"] or ""))

        return params

    def submit(self, button):
        action = button["formaction"] if button and button["formaction"] else self.native.get("action")
        method = self._request_method
        self.driver.submit(method, action, self.params(button))

    @property
    def _request_method(self):
        if self["method"] and re.compile(r"post", re.IGNORECASE).search(self["method"]):
            return "POST"
        else:
            return "GET"

    @property
    def _multipart(self):
        return self["enctype"] == "multipart/form-data"
