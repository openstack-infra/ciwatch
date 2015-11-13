/* Copyright (c) 2015 Tintri. All rights reserved.
 *
 *    Licensed under the Apache License, Version 2.0 (the "License"); you may
 *    not use this file except in compliance with the License. You may obtain
 *    a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 *    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 *    License for the specific language governing permissions and limitations
 *    under the License.
 */

var toggle_verified_plus = function () {
  var color = "#BFA";
  if ($(this).hasClass("active")){
    color = "";
  }
  $(".verified1").css("background-color", color);
}

var toggle_verified_minus = function () {
  var color = "#FAA";
  if ($(this).hasClass("active")){
    color = "";
  }
  $(".verified-1").css("background-color", color);
}


$(document).ready(function () {
  $("colgroup").each(function (i, elem) {
    if ($(elem).hasClass("verified-1")) {
      $("#results").find("td").filter(":nth-child(" + (i + 1) + ")").addClass("verified-1");
    } else if ($(elem).hasClass("verified1")) {
      $("#results").find("td").filter(":nth-child(" + (i + 1) + ")").addClass("verified1");
    }
  });
  $("#verified1-button").on("click", toggle_verified_plus);
  $("#verified-1-button").on("click", toggle_verified_minus);
});
