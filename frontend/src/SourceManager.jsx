import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import TextSnippetIcon from '@mui/icons-material/TextSnippet';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

/* eslint-disable react/prop-types */
export const SourceManager = ({ rows, sha256, downloadTemplate, uploadSource }) => {
  return <>
    <Typography variant="h4" gutterBottom textAlign={'center'}>
      Examly - Generatore di test automatico
    </Typography>
    <Box textAlign={'center'}>
      <Button variant='contained' startIcon={<TextSnippetIcon />} color='success' sx={{ m: 1 }} onClick={downloadTemplate}>
        Scarica template per le domande
      </Button>
      <Button component="label" tabIndex={-1} role={undefined} variant='contained' startIcon={<UploadFileIcon />} sx={{ m: 1 }}>
        Carica sorgente delle domande
        <VisuallyHiddenInput type="file" onChange={uploadSource} />
      </Button>
    </Box>
    <Typography variant="h6" gutterBottom sx={{ m: 1, textAlign: 'center', color: "grey" }}>
      Domande analizzate: {rows}
    </Typography>
    <Typography variant="h6" gutterBottom sx={{ m: 1, textAlign: 'center', color: "grey" }}>
      SHA256 sorgente: {sha256}
    </Typography>
  </>
};