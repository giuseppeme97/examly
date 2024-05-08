export const writeDownloadedFile = async (response, fileName) => {
    const downloadUrl = URL.createObjectURL(await response.blob());
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(downloadUrl);
};