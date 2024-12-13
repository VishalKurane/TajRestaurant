// fetchAndRenderMenu();
let AZ_FUNCTION_GET_MENU; // Declare the variable globally

// Fetch the configuration dynamically
async function fetchConfig() {
  try {
    const response = await fetch("/config");
    if (!response.ok) {
      throw new Error(`Failed to fetch config: ${response.status}`);
    }
    const config = await response.json();
    AZ_FUNCTION_GET_MENU = config.AZ_FUNCTION_GET_MENU;

    // Debug: Check if the variable is set correctly
    console.log("Menu API URL from config:", AZ_FUNCTION_GET_MENU);

    if (!AZ_FUNCTION_GET_MENU) {
      throw new Error("AZ_FUNCTION_GET_MENU is undefined in the config response.");
    }

    // Proceed to fetch and render the menu after config is loaded
    await fetchAndRenderMenu();
  } catch (error) {
    console.error("Error fetching config or AZ_FUNCTION_GET_MENU:", error);
  }
}

// Function to fetch API data and render it
async function fetchAndRenderMenu() {
  if (!AZ_FUNCTION_GET_MENU) {
    console.error("AZ_FUNCTION_GET_MENU is not defined");
    return; // Exit if the variable is undefined
  }

  try {
    const response = await fetch(AZ_FUNCTION_GET_MENU);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const apiData = await response.json();

    // Debugging: Log API response
    console.log("API Response:", apiData);

    // Transform the API data to match the rendering logic
    const menuData = apiData.map((category) => ({
      category: category.Category,
      items: category.Menus.map((menu) => ({
        name: menu.name,
        description: menu.description,
        price: menu.price,
        image: menu.image_url || "https://via.placeholder.com/60", // Fallback image
      })),
    }));

    // Debugging: Log transformed menuData
    console.log("Transformed menuData:", menuData);

    // Render the transformed menuData
    renderMenu(menuData);
  } catch (error) {
    console.error("Error fetching or processing menu data:", error);
  }
}

// Rendering menuData into the DOM
function renderMenu(menuData) {
  const menuSection = document.getElementById("menu-section");

  // Clear the menu section first
  menuSection.innerHTML = "";

  menuData.forEach((category) => {
    // Create a block for each category
    const categoryBlock = document.createElement("div");
    categoryBlock.classList.add("menu-category");

    const categoryTitle = document.createElement("h3");
    categoryTitle.innerText = category.category;
    categoryBlock.appendChild(categoryTitle);

    // Render up to 8 items per category
    category.items.slice(0, 8).forEach((item) => {
      const menuItem = document.createElement("div");
      menuItem.classList.add("menu-item");

      // Create and append image
      const itemImage = document.createElement("img");
      itemImage.src = item.image;
      itemImage.alt = item.name;
      menuItem.appendChild(itemImage);

      // Create and append details
      const itemDetails = document.createElement("div");
      itemDetails.classList.add("menu-details");

      const itemName = document.createElement("h4");
      itemName.innerText = item.name;
      itemDetails.appendChild(itemName);

      const itemDescription = document.createElement("p");
      itemDescription.innerText = item.description;
      itemDetails.appendChild(itemDescription);

      // Create and append price with hover effect
      const itemPrice = document.createElement("p");
      itemPrice.classList.add("price");
      itemPrice.innerText = `₹${item.price}`;
      itemDetails.appendChild(itemPrice);

      menuItem.appendChild(itemDetails);
      categoryBlock.appendChild(menuItem);
    });

    menuSection.appendChild(categoryBlock);
  });
}

// Trigger the config fetch process
fetchConfig();