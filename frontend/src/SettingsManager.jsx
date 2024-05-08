import { useState } from 'react';
import TextField from '@mui/material/TextField';
import DescriptionIcon from '@mui/icons-material/Description';
import FolderZipIcon from '@mui/icons-material/FolderZip';
import InputAdornment from '@mui/material/InputAdornment';
import TitleIcon from '@mui/icons-material/Title';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Select from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import Chip from '@mui/material/Chip';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import ListIcon from '@mui/icons-material/List';
import AssignmentIcon from '@mui/icons-material/Assignment';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';


/* eslint-disable react/prop-types */
export const SettingsManager = ({ subjects, classrooms, start }) => {
  const [fileName, setFileName] = useState("exam");
  const [zipName, setZipName] = useState("zip");
  const [documentTitle, setDocumentTitle] = useState("Compito di Sistemi e Reti - A.S. 2023/2024 - Classe 3F");
  const [selectedSubjects, setSelectedSubjects] = useState([]);
  const [selectedClassrooms, setSelectedClassrooms] = useState([]);
  const [numberOfExams, setNumberOfExams] = useState(5);
  const [numberOfQuestions, setNumberOfQuestions] = useState(40);
  const [numberOfOptions, setNumberOfOptions] = useState(4);
  const [numberOnDocument, setNumberOnDocument] = useState(false);
  const [numberOnQuestions, setNumberOnQuestions] = useState(false);
  const [shuffleQuestions, setShuffleQuestions] = useState(true);
  const [shuffleOptions, setShuffleOptions] = useState(true);
  const [singleInclusion, setSingleInclusion] = useState(false);
  const [exportSolutions, setExportSolutions] = useState(true);


  const handleFileName = (event) => {
    setFileName(event.target.value);
  };

  const handleZipName = (event) => {
    setZipName(event.target.value);
  };

  const handleDocumentTitle = (event) => {
    setDocumentTitle(event.target.value);
  };

  const handleSubjects = (event) => {
    setSelectedSubjects(
      typeof event.target.value === 'string' ? event.target.value.split(',') : event.target.value,
    );
  };

  const handleClassrooms = (event) => {
    setSelectedClassrooms(
      typeof event.target.value === 'string' ? event.target.value.split(',') : event.target.value,
    );
  };

  const handleNumberOfExams = (event) => {
    setNumberOfExams(event.target.value);
  };

  const handleNumberOfQuestions = (event) => {
    setNumberOfQuestions(event.target.value);
  };

  const handleNumberOfOptions = (event) => {
    setNumberOfOptions(event.target.value);
  };

  const handleNumberOnDocument = () => {
    setNumberOnDocument(!numberOnDocument);
  };

  const handleNumberOnQuestions = () => {
    setNumberOnQuestions(!numberOnQuestions);
  };

  const handleShuffleQuestions = () => {
    setShuffleQuestions(!shuffleQuestions);
  };

  const handleSetShuffleOptions = () => {
    setShuffleOptions(!shuffleOptions);
  };

  const handleSingleInclusion = () => {
    setSingleInclusion(!singleInclusion);
  };

  const handleExportSolutions = () => {
    setExportSolutions(!exportSolutions);
  };

  const handleStart = () => {
    let settings = {
      fileName,
      zipName,
      documentTitle,
      selectedSubjects,
      selectedClassrooms,
      numberOfExams,
      numberOfQuestions,
      numberOnDocument,
      numberOnQuestions,
      shuffleQuestions,
      shuffleOptions,
      exportSolutions,
      singleInclusion
    };

    start(settings);
  };

  const checkSettings = () => {
    return ((fileName !== "") &&
      (zipName !== "") &&
      (documentTitle !== "") &&
      (selectedSubjects.length > 0) &&
      (selectedClassrooms.length > 0) &&
      (numberOfExams > 0) &&
      (numberOfQuestions > 0))
  };

  return <>
    <TextField
      required
      value={fileName}
      onChange={handleFileName}
      placeholder='exam'
      label="Nome file"
      sx={{ m: 1 }}
      InputProps={{
        startAdornment: <InputAdornment position="start"><DescriptionIcon></DescriptionIcon></InputAdornment>,
      }}
    />
    <TextField
      required
      value={zipName}
      onChange={handleZipName}
      placeholder='exam'
      label="Nome zip"
      sx={{ m: 1 }}
      InputProps={{
        startAdornment: <InputAdornment position="start"><FolderZipIcon></FolderZipIcon></InputAdornment>,
      }}
    />
    <br />
    <FormControl sx={{ m: 1, width: 300 }} >
      <InputLabel>Materie</InputLabel>
      <Select
        multiple
        value={selectedSubjects}
        onChange={handleSubjects}
        input={<OutlinedInput label="Materie" />}
        renderValue={(selected) => (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {selected.map((value) => (
              <Chip key={value} label={value} />
            ))}
          </Box>
        )}
      >
        {subjects.map((name) => (
          <MenuItem key={name} value={name}>
            <Checkbox checked={selectedSubjects.indexOf(name) > -1} />
            <ListItemText primary={name} />
          </MenuItem>
        ))}
      </Select>
    </FormControl>
    <FormControl sx={{ m: 1, width: 300 }}>
      <InputLabel>Classi</InputLabel>
      <Select
        multiple
        value={selectedClassrooms}
        onChange={handleClassrooms}
        input={<OutlinedInput label="Classi" />}
        renderValue={(selected) => (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {selected.map((value) => (
              <Chip key={value} label={value} />
            ))}
          </Box>
        )}
      >
        {classrooms.map((name) => (
          <MenuItem key={name} value={name}>
            <Checkbox checked={selectedClassrooms.indexOf(name) > -1} />
            <ListItemText primary={name} />
          </MenuItem>
        ))}
      </Select>
    </FormControl>
    <br />
    <TextField
      required
      value={documentTitle}
      onChange={handleDocumentTitle}
      placeholder='Compito di Sistemi e Reti - A.S. 2023/2024 - Classe 3F'
      label="Titolo documento"
      sx={{ m: 1, width: 500 }}
      InputProps={{
        startAdornment: <InputAdornment position="start"><TitleIcon></TitleIcon></InputAdornment>,
      }}
    />
    <br />
    <TextField
      value={numberOfExams}
      error={numberOfExams <= 0}
      onChange={handleNumberOfExams}
      label="Numero di esami"
      type="number"
      sx={{ m: 1 }}
      InputProps={{
        startAdornment: <InputAdornment position="start"><FileCopyIcon /></InputAdornment>,
      }}
      InputLabelProps={{
        shrink: true,
      }}
    />
    <TextField
      value={numberOfQuestions}
      error={numberOfQuestions <= 0}
      onChange={handleNumberOfQuestions}
      label="Numero di domande"
      type="number"
      sx={{ m: 1 }}
      //ok
      InputProps={{
        startAdornment: <InputAdornment position="start"><ListIcon /></InputAdornment>,
      }}
      InputLabelProps={{
        shrink: true,
      }}
    />

    <hr />

    <TextField
      value={numberOfOptions}
      onChange={handleNumberOfOptions}
      label="Numero di opzioni"
      type="number"
      disabled
      sx={{ m: 1, display: 'none' }}
      InputLabelProps={{
        shrink: true,
      }}
    />
    <FormGroup sx={{ m: 1 }}>
      <FormControlLabel control={<Checkbox checked={numberOnDocument} onChange={handleNumberOnDocument} />} label="Numera documenti" />
      <FormControlLabel control={<Checkbox checked={numberOnQuestions} onChange={handleNumberOnQuestions} />} label="Numera domande" />
      <FormControlLabel control={<Checkbox checked={shuffleQuestions} onChange={handleShuffleQuestions} />} label="Mescola domande" />
      <FormControlLabel control={<Checkbox checked={shuffleOptions} onChange={handleSetShuffleOptions} />} label="Mescola opzioni" />
      <FormControlLabel control={<Checkbox checked={singleInclusion} onChange={handleSingleInclusion} />} label="Singola inclusione" />
      <FormControlLabel control={<Checkbox checked={exportSolutions} onChange={handleExportSolutions} />} label="Esporta correttori" />
    </FormGroup>
    <Box textAlign={'center'}>
      <Button onClick={handleStart} variant='contained' disabled={!checkSettings()} startIcon={<AssignmentIcon />} color='error' sx={{ m: 1 }}>
        Genera esami!
      </Button>
    </Box>
  </>
};