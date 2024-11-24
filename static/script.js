const apiUrl = "http://127.0.0.1:8000"; // Backend API URL

// Fetch and render all categories
async function loadCategories() {
    try {
        const response = await fetch(`${apiUrl}/categories`);
        const categories = await response.json();
        console.log("Categories fetched:", categories);

        const categoriesDiv = document.getElementById("categories");
        categoriesDiv.innerHTML = ""; // Clear existing content

        categories.forEach(category => {
            const categoryDiv = document.createElement("div");
            categoryDiv.className = "category";

            categoryDiv.innerHTML = `
                <span>${category.name} - ${category.time} hours</span>
                <button onclick="updateCategoryTime(${category.id}, 1)">+</button>
                <button onclick="updateCategoryTime(${category.id}, -1)">-</button>
            `;

            categoriesDiv.appendChild(categoryDiv);
        });
    } catch (error) {
        console.error("Error loading categories:", error);
    }
}

// Update time for a category
async function updateCategoryTime(categoryId, timeChange) {
    try {
        const response = await fetch(`${apiUrl}/categories/${categoryId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ time: timeChange }),
        });

        if (!response.ok) {
            throw new Error("Failed to update time");
        }

        loadCategories(); // Reload categories after update
    } catch (error) {
        console.error("Error updating category time:", error);
    }
}

// Create a new category
async function createNewCategory() {
    const categoryName = document.getElementById("new-category-name").value;

    if (!categoryName) {
        alert("Please enter a category name!");
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/categories`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: categoryName }),
        });

        if (!response.ok) {
            throw new Error("Failed to create category");
        }

        document.getElementById("new-category-name").value = ""; // Clear input
        loadCategories(); // Reload categories
    } catch (error) {
        console.error("Error creating category:", error);
    }
}

// Load categories on page load
loadCategories();
