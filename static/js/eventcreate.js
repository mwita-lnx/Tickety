$(document).ready(function () {
    // Show the modal when "Add Category" button is clicked
    $("#addCategory").click(function () {
        $("#categoryModal").modal("show");
    });

    // Function to handle category deletion
    function handleDelete() {
        $(this).closest(".categories").remove();
    }

    // Save the category and price when "Save" button is clicked
    $("#saveCategory").click(function () {
        const categoryName = $("#categoryName").val();
        const categoryPrice = $("#categoryPrice").val();

        if (categoryPrice) {
            const categoryDiv = $('<div class="categories row col-sm-3">');
            const label = $('<div for="id_value" class="form-label">').text(`${categoryName}:`);
            const input = $(`<br><input type="number"  id="id_value" name="${categoryName}" class="form-control col-sm-8">`).val(categoryPrice);
            const deleteButton = $('<button style="height:40px" class="btn btn-danger  btn-sm">x</button>').click(handleDelete);

            categoryDiv.append(label, input, deleteButton);

            // Append the category div to the container
            $(".categories-container").append(categoryDiv);

            // Clear input fields
            $("#categoryName").val("");
            $("#categoryPrice").val("");

            // Close the modal
            $("#categoryModal").modal("hide");
        }
    });

    // Prevent the form from submitting for demo purposes
    $("#eventForm").submit(function (e) {
        e.preventDefault();

        // You can submit the form data to your server here
        console.log("Form submitted with data:", $(this).serialize());
    });
});

function handleSucces(url) {
    $("#successModal").modal("show");
    // Handle the redirect when the "Redirect" button is clicked
    setTimeout(function () {
        $("#successModal").modal("hide");
    }, 1500);
}

function apiHandler(url, data, successCallback, errorCallback) {
    const form_data = new FormData();
    for (var key in data) {
        form_data.append(key, data[key]);
    }

    const csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: url, // Use the provided URL
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        headers: { "X-CSRFToken": csrftoken },
        success: function (response) {
            if (typeof successCallback === 'function') {
                successCallback(response);
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            if (typeof errorCallback === 'function') {
                errorCallback(xhr.responseText, textStatus, errorThrown);
            }
        },
    });
}

function convertTo24HourFormat(time12hr) {
    // Split the time into hours, minutes, and period (AM/PM)
    console.log(time12hr)
    const [timePart, period] = time12hr.split(' ');
    const [hours, minutes] = timePart.split(':').map(Number);

    // Convert hours to 24-hour format
    let hours24 = hours;

    // Adjust hours for PM
    if (period === 'PM' && hours !== 12) {
        hours24 += 12;
    }

    // Handle midnight (12:00 AM) as 00:00 in 24-hour format
    if (period === 'AM' && hours === 12) {
        hours24 = 0;
    }

    // Format the time in 24-hour format
    const time24hr = `${String(hours24).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;

    return time24hr;
}
function convertDateFormat(inputDate) {
    // Split the input date into parts (month, day, and year)
    const dateParts = inputDate.split('-');
    if (dateParts.length === 3) {
        // Rearrange the parts to the "yyyy-mm-dd" format
        const year = dateParts[0];
        const month = dateParts[2].padStart(2, '0'); // Ensure 2-digit month
        const day = dateParts[1].padStart(2, '0'); // Ensure 2-digit day

        // Construct the converted date in "yyyy-mm-dd" format
        const convertedDate = `${year}-${day}-${month}`;
        return convertedDate;
    } else {
        return null; // Invalid input format
    }
}
handleSucces('s')
// Example usage:
$(document).ready(function () {
    $("#upload").on("submit", function (e) {
        e.preventDefault(); // Prevent the default form submission behavior

        var data = {
            title: $("#id_title").val(),
            thumbnail: null,
            about: $("#id_about").val(),
            ticket_size: parseInt($("#id_ticket_size").val()),
            location: $("#id_location").val(),
            start_date: convertDateFormat($("#id_start_date").val()),
            start_time: convertTo24HourFormat($("#id_start_time").val()), // Switched
            end_time: convertTo24HourFormat($("#id_end_time").val()), // Switched
            end_date: convertDateFormat($("#id_end_date").val()), // Switched
        };


        var fileInput = $("#id_thumbnail")[0].files[0];
        data.thumbnail = fileInput;
        console.log(data)
        apiHandler("/api/event/create", data, (response) => {
            $(".categories-container").find(".categories").each(function (index) {
                // Extract categoryname and value from each category element
                var categoryName = $(this).find("input").attr("name");
                var categoryValue = $(this).find("input").val().trim();
                let cat_data = {
                    category_name: categoryName,
                    value: categoryValue,
                    event: response.id
                }
                apiHandler("/api/category/create", cat_data, (response) => {
                    console.log(response)
                }, () => { })
                handleSucces('ur')
            });
            console.log(response)
        }, (response) => { })


    });
});