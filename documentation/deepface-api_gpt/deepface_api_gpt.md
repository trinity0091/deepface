




## how to run



https://github.com/trinityzhub/deepface

how to start 
```




pip install deepface

sudo apt-get update
sudo apt-get install libgl1-mesa-glx



pip install -r requirements.txt




python api/api.py -p 5000


```





## how to call



http://localhost:5000/analyze
https://5000-trinityzhub-deepface-05rg8w99g1h.ws-us103.gitpod.io/analyze
POST

       {
         "img": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE..."]
       }



http://localhost:5000/represent
https://5000-trinityzhub-deepface-05rg8w99g1h.ws-us103.gitpod.io/represent
POST

       {
         "img": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE..."
       }













http://localhost:5000/analyze
https://5000-trinityzhub-deepface-05rg8w99g1h.ws-us103.gitpod.io/analyze
POST

       {
         "img": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE..."]
       }



http://localhost:5000/represent
https://5000-trinityzhub-deepface-05rg8w99g1h.ws-us103.gitpod.io/represent
POST

       {
         "img": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE..."
       }




## Images for example


```base64
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtC
ohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=

```






```base64


```











## GPT 





how to run api/api.py of deepface project  "https://github.com/serengil/deepface"
explain in step wise



Running the `api.py` script from the DeepFace project involves setting up a Flask web server that exposes APIs for facial analysis, verification, and embedding generation. Below are the step-by-step instructions to run the `api.py` script:

1. **Clone the DeepFace Repository**:
   Clone the DeepFace GitHub repository to your local machine:
   ```bash
   git clone https://github.com/serengil/deepface.git
   ```

2. **Navigate to the Project Directory**:
   Change your working directory to the cloned DeepFace project folder:
   ```bash
   cd deepface
   ```

3. **Install Dependencies**:
   Install the required Python packages using pip. It's recommended to use a virtual environment to avoid conflicts with other packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API Server**:
   Run the `api.py` script using Python. You can specify the port number as an argument. The default port is 5000, but you can choose a different one if needed:
   ```bash
   python api/api.py -p 5000
   ```
   The `-p` option specifies the port number for the Flask web server. Make sure the specified port is not already in use.

5. **Access the API Endpoints**:
   Once the server is running, you can access the following API endpoints using tools like `curl`, `Postman`, or by sending HTTP requests programmatically using a programming language of your choice:

   - **Analyze Endpoint**: Analyze facial attributes (emotion, age, gender, race) from images.
     - URL: `http://localhost:5000/analyze`
     - Method: POST
     - Request Format: JSON containing an array of image URLs or base64 encoded images. Example request:
       ```json
       {
         "img": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE..."]
       }
       ```
   - **Verify Endpoint**: Verify if two images belong to the same person.
     - URL: `http://localhost:5000/verify`
     - Method: POST
     - Request Format: JSON containing an array of image pairs. Each pair should contain `img1` and `img2` keys with base64 encoded images. Example request:
       ```json
       {
         "img": [
           {"img1": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE...", "img2": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE..."}
         ]
       }
       ```
   - **Represent Endpoint**: Generate embeddings for facial images.
     - URL: `http://localhost:5000/represent`
     - Method: POST
     - Request Format: JSON containing a single base64 encoded image. Example request:
       ```json
       {
         "img": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE..."
       }
       ```

6. **Interact with the APIs**:
   You can use tools like `curl`, `Postman`, or your preferred programming language to interact with the API endpoints. For example, you can send POST requests with the required JSON payloads to analyze, verify, or generate embeddings for facial images.

Remember that this guide assumes you have Python and the necessary dependencies installed. Also, make sure to handle any security considerations if you plan to expose the API to the internet.
















The error message you are encountering is related to the missing `libGL.so.1` shared library, which is required by the OpenCV library used in the DeepFace project. This library is used for handling graphics-related operations. To resolve this issue, you can follow these steps:

1. **Install Required Dependencies**:

   On Ubuntu/Debian-based systems, you can install the necessary dependencies using the following command:

   ```bash
   sudo apt-get update
   sudo apt-get install libgl1-mesa-glx
   ```

   On CentOS/Fedora-based systems, use the following command:

   ```bash
   sudo yum install mesa-libGL
   ```

2. **Re-run the Script**:

   After installing the required library, try running the `api.py` script again:

   ```bash
   python api/api.py -p 5000
   ```

This should resolve the `libGL.so.1` missing shared library error. If you encounter any other issues or errors, please provide more information about the error message, and I'll be happy to assist you further.














