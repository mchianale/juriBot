import requests

def queryInformationsBySimilarity(n_results : int, query : str):
        query_data = {
            "query": query,
            "n_results": n_results,
            "include": ['documents', 'metadatas']
        }

        response = requests.get("http://vector-similarity-api:8001/query", json=query_data)
        if response.status_code == 200:
            # Decode the response content as JSON
            response_json = response.json().get('results')

            # Extract documents and metadata from the response
            documents = response_json.get('documents', [])[0]
            metadatas = response_json.get('metadatas', [])[0]

            # Prepare the results
            results = []
            for i in range(len(documents)):
                results.append({
                    "document": documents[i],
                    "metadata": metadatas[i]
                })

            return f"{results}"
        else:
            # If the response is not successful, return the error content
            return f"error: {response.status_code}, message: {response.text}"
        

