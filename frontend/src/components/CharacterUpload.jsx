import { useState } from "react"

function CharacterUpload() {

    const [loading, setLoading] = useState(false)
    const [selectedFile, setSelectedFile] = useState(null)
    const [imageUrls, setImageUrls] = useState([])
    
    

    const handleSubmit = async () => {
        if (!selectedFile) {
            alert('Please select an image first');
            return;
        }
        setLoading(true)
        try {
            const formData = new FormData()
            formData.append("image", selectedFile)

            const response = await fetch('http://127.0.0.1:8000/generate', {
                method: 'POST',
                body: formData
                }
            );

            const data = await response.json();
            console.log('Img urls recieved:', data);
            setImageUrls(data.images)

        }

        catch (error) {
            console.error('Error generating images:', error);
            alert('Failed to generate Images');
        }
        finally {
            setLoading(false)
        }

    };
    
    return (
        <>
            <form>
                <label>
                    {selectedFile ? selectedFile.name : 'Choose Image'}
                    <input type="file"
                    accept='image/*'
                    onChange={(event) => setSelectedFile(event.target.files[0])}
                    />
                </label>
                <button onClick={handleSubmit}> Submit </button>
            </form>
            
            <div>
               {imageUrls.map((url, index) => (
                    <img key={index} src={url} alt='generated image' />
               ))} 
            </div>
            {loading && <p>Generating views...</p>}
        </>
    )
}



export default CharacterUpload

