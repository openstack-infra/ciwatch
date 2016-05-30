$(document).ready(function () {
  $("td.ci-name").parent().click(function () {
    $(this).toggleClass("selected");
  });

  $("#select-button").click(function () {
    if ($(this).hasClass("active")) {
      $("tr:hidden,tbody:hidden").show();
      $(this).color = "";
      $(this).html("Select");
    } else {
      $("tr:not(.selected):has(td.ci-name)").hide();
      $("tbody:not(:has(.selected),:not(:has(td.ci-name)))").hide();
      $(".selected").removeClass("selected");

      $(this).html("Unselect");
    }
  });
});

