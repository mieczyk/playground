import matplotlib.pyplot as plt
import numpy as np

# Code snippet taken from the article "Principal Component Analysis Made Easy: A Step-by-Step Tutorial"
# by Marcus Sena
# Source URL: https://medium.com/data-science/principal-component-analysis-made-easy-a-step-by-step-tutorial-184f295e97fe

class PCA:
    def __init__(self, k: int) -> None:
        """
        Initialize the PCA algorithm.

        k - number of desired components.
        """
        self.k = k
        self.components = None
        self.mean = None
        self.explained_variance = None

    def fit(self, input_data: np.ndarray) -> None:
        """
        Prepare data for final transformation data into low-dimensional space.

        input_data - original data's matrix.        
        """
        # 1. Standarize the input data (subtract the mean).
        self.mean = np.mean(input_data, axis=0)
        centered_input_data = input_data - self.mean

        # 2. Compute the covariance matrix
        # Argument `rowvar = False` means the relationship is transposed, i.e. 
        # each column represents a variable and the rows contains observations.
        cov_matrix = np.cov(centered_input_data, rowvar=False)

        # 3. Compute the eigenvectors and eigenvalues for the covariance matrix.
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

        # 4. Sort the eigenvalues and the corresponding eigenvectors.
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]

        # 5. Select the top k components and calculate explained variance.
        self.components = eigenvectors[:, :self.k]
        total_variance = np.sum(eigenvalues)
        self.explained_variance = eigenvalues[:self.k] / total_variance

    def transform(self, input_data):
        """
        Project input data onto the calculated dimensions (reduced).
        """
        # 6. Project the input data onto the selected components.
        centered_input_data = input_data - self.mean
        return np.dot(centered_input_data, self.components)
    
    def plot_explained_variance(self):
        """
        Show the explained variance of each selected principal component on the plot.
        """
        # Create labels for each principal component.
        labels = [f"PCA{i+1}" for i in range(self.k)]

        # Create a bar plot for explained variance.
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, self.k + 1), self.explained_variance, alpha=0.7, align='center', color='blue', tick_label=labels)
        plt.xlabel('Principal Component')
        plt.ylabel('Explained Variance Ratio')
        plt.title('Explained Variance by Principal Components')
        plt.show()


def generate_random_dataset(samples_count: int, features_count: int, k: int):
    """
    Generates random dataset that meets PCA algorithm's assumptions
    """
    if k > features_count:
        raise ValueError(f"Desired dimensionality k={k} cannot be larger than original dimensionality features_count={features_count}")

    np.random.seed(None)

    # Generate a low-dimensional signal.
    low_dim_data = np.random.randn(samples_count, k)
    
    # Create a random projection matrix to project into higher dimensions
    projection_matrix = np.random.randn(k, features_count)

    # Project the low-dimensional data to higher dimensions
    high_dim_data = np.dot(low_dim_data, projection_matrix)

    # Add some noise to the high-dimensional data
    noise = np.random.normal(loc=0, scale=0.5, size=(samples_count, fea tures_count))
    data_with_noise = high_dim_data + noise

    return data_with_noise


if __name__ == "__main__":
    k = 4
    
    input_data = generate_random_dataset(100, 10, k)
    
    pca = PCA(k)
    pca.fit(input_data)
    transformed_input_data = pca.transform(input_data)
    
    print("Explained Variance:\n", pca.explained_variance)
    pca.plot_explained_variance()