import essentia
import essentia.standard as es
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D
import numpy as np


def get_audio_features(file_directory):

    try:
        track_features = []

        # ----------------------- Embeddings -----------------------
        labels = ["Blues---Boogie Woogie",
                "Blues---Chicago Blues",
                "Blues---Country Blues",
                "Blues---Delta Blues",
                "Blues---Electric Blues",
                "Blues---Harmonica Blues",
                "Blues---Jump Blues",
                "Blues---Louisiana Blues",
                "Blues---Modern Electric Blues",
                "Blues---Piano Blues",
                "Blues---Rhythm & Blues",
                "Blues---Texas Blues",
                "Brass & Military---Brass Band",
                "Brass & Military---Marches",
                "Brass & Military---Military",
                "Children's---Educational",
                "Children's---Nursery Rhymes",
                "Children's---Story",
                "Classical---Baroque",
                "Classical---Choral",
                "Classical---Classical",
                "Classical---Contemporary",
                "Classical---Impressionist",
                "Classical---Medieval",
                "Classical---Modern",
                "Classical---Neo-Classical",
                "Classical---Neo-Romantic",
                "Classical---Opera",
                "Classical---Post-Modern",
                "Classical---Renaissance",
                "Classical---Romantic",
                "Electronic---Abstract",
                "Electronic---Acid",
                "Electronic---Acid House",
                "Electronic---Acid Jazz",
                "Electronic---Ambient",
                "Electronic---Bassline",
                "Electronic---Beatdown",
                "Electronic---Berlin-School",
                "Electronic---Big Beat",
                "Electronic---Bleep",
                "Electronic---Breakbeat",
                "Electronic---Breakcore",
                "Electronic---Breaks",
                "Electronic---Broken Beat",
                "Electronic---Chillwave",
                "Electronic---Chiptune",
                "Electronic---Dance-pop",
                "Electronic---Dark Ambient",
                "Electronic---Darkwave",
                "Electronic---Deep House",
                "Electronic---Deep Techno",
                "Electronic---Disco",
                "Electronic---Disco Polo",
                "Electronic---Donk",
                "Electronic---Downtempo",
                "Electronic---Drone",
                "Electronic---Drum n Bass",
                "Electronic---Dub",
                "Electronic---Dub Techno",
                "Electronic---Dubstep",
                "Electronic---Dungeon Synth",
                "Electronic---EBM",
                "Electronic---Electro",
                "Electronic---Electro House",
                "Electronic---Electroclash",
                "Electronic---Euro House",
                "Electronic---Euro-Disco",
                "Electronic---Eurobeat",
                "Electronic---Eurodance",
                "Electronic---Experimental",
                "Electronic---Freestyle",
                "Electronic---Future Jazz",
                "Electronic---Gabber",
                "Electronic---Garage House",
                "Electronic---Ghetto",
                "Electronic---Ghetto House",
                "Electronic---Glitch",
                "Electronic---Goa Trance",
                "Electronic---Grime",
                "Electronic---Halftime",
                "Electronic---Hands Up",
                "Electronic---Happy Hardcore",
                "Electronic---Hard House",
                "Electronic---Hard Techno",
                "Electronic---Hard Trance",
                "Electronic---Hardcore",
                "Electronic---Hardstyle",
                "Electronic---Hi NRG",
                "Electronic---Hip Hop",
                "Electronic---Hip-House",
                "Electronic---House",
                "Electronic---IDM",
                "Electronic---Illbient",
                "Electronic---Industrial",
                "Electronic---Italo House",
                "Electronic---Italo-Disco",
                "Electronic---Italodance",
                "Electronic---Jazzdance",
                "Electronic---Juke",
                "Electronic---Jumpstyle",
                "Electronic---Jungle",
                "Electronic---Latin",
                "Electronic---Leftfield",
                "Electronic---Makina",
                "Electronic---Minimal",
                "Electronic---Minimal Techno",
                "Electronic---Modern Classical",
                "Electronic---Musique Concr\u00e8te",
                "Electronic---Neofolk",
                "Electronic---New Age",
                "Electronic---New Beat",
                "Electronic---New Wave",
                "Electronic---Noise",
                "Electronic---Nu-Disco",
                "Electronic---Power Electronics",
                "Electronic---Progressive Breaks",
                "Electronic---Progressive House",
                "Electronic---Progressive Trance",
                "Electronic---Psy-Trance",
                "Electronic---Rhythmic Noise",
                "Electronic---Schranz",
                "Electronic---Sound Collage",
                "Electronic---Speed Garage",
                "Electronic---Speedcore",
                "Electronic---Synth-pop",
                "Electronic---Synthwave",
                "Electronic---Tech House",
                "Electronic---Tech Trance",
                "Electronic---Techno",
                "Electronic---Trance",
                "Electronic---Tribal",
                "Electronic---Tribal House",
                "Electronic---Trip Hop",
                "Electronic---Tropical House",
                "Electronic---UK Garage",
                "Electronic---Vaporwave",
                "Folk, World, & Country---African",
                "Folk, World, & Country---Bluegrass",
                "Folk, World, & Country---Cajun",
                "Folk, World, & Country---Canzone Napoletana",
                "Folk, World, & Country---Catalan Music",
                "Folk, World, & Country---Celtic",
                "Folk, World, & Country---Country",
                "Folk, World, & Country---Fado",
                "Folk, World, & Country---Flamenco",
                "Folk, World, & Country---Folk",
                "Folk, World, & Country---Gospel",
                "Folk, World, & Country---Highlife",
                "Folk, World, & Country---Hillbilly",
                "Folk, World, & Country---Hindustani",
                "Folk, World, & Country---Honky Tonk",
                "Folk, World, & Country---Indian Classical",
                "Folk, World, & Country---La\u00efk\u00f3",
                "Folk, World, & Country---Nordic",
                "Folk, World, & Country---Pacific",
                "Folk, World, & Country---Polka",
                "Folk, World, & Country---Ra\u00ef",
                "Folk, World, & Country---Romani",
                "Folk, World, & Country---Soukous",
                "Folk, World, & Country---S\u00e9ga",
                "Folk, World, & Country---Volksmusik",
                "Folk, World, & Country---Zouk",
                "Folk, World, & Country---\u00c9ntekhno",
                "Funk / Soul---Afrobeat",
                "Funk / Soul---Boogie",
                "Funk / Soul---Contemporary R&B",
                "Funk / Soul---Disco",
                "Funk / Soul---Free Funk",
                "Funk / Soul---Funk",
                "Funk / Soul---Gospel",
                "Funk / Soul---Neo Soul",
                "Funk / Soul---New Jack Swing",
                "Funk / Soul---P.Funk",
                "Funk / Soul---Psychedelic",
                "Funk / Soul---Rhythm & Blues",
                "Funk / Soul---Soul",
                "Funk / Soul---Swingbeat",
                "Funk / Soul---UK Street Soul",
                "Hip Hop---Bass Music",
                "Hip Hop---Boom Bap",
                "Hip Hop---Bounce",
                "Hip Hop---Britcore",
                "Hip Hop---Cloud Rap",
                "Hip Hop---Conscious",
                "Hip Hop---Crunk",
                "Hip Hop---Cut-up/DJ",
                "Hip Hop---DJ Battle Tool",
                "Hip Hop---Electro",
                "Hip Hop---G-Funk",
                "Hip Hop---Gangsta",
                "Hip Hop---Grime",
                "Hip Hop---Hardcore Hip-Hop",
                "Hip Hop---Horrorcore",
                "Hip Hop---Instrumental",
                "Hip Hop---Jazzy Hip-Hop",
                "Hip Hop---Miami Bass",
                "Hip Hop---Pop Rap",
                "Hip Hop---Ragga HipHop",
                "Hip Hop---RnB/Swing",
                "Hip Hop---Screw",
                "Hip Hop---Thug Rap",
                "Hip Hop---Trap",
                "Hip Hop---Trip Hop",
                "Hip Hop---Turntablism",
                "Jazz---Afro-Cuban Jazz",
                "Jazz---Afrobeat",
                "Jazz---Avant-garde Jazz",
                "Jazz---Big Band",
                "Jazz---Bop",
                "Jazz---Bossa Nova",
                "Jazz---Contemporary Jazz",
                "Jazz---Cool Jazz",
                "Jazz---Dixieland",
                "Jazz---Easy Listening",
                "Jazz---Free Improvisation",
                "Jazz---Free Jazz",
                "Jazz---Fusion",
                "Jazz---Gypsy Jazz",
                "Jazz---Hard Bop",
                "Jazz---Jazz-Funk",
                "Jazz---Jazz-Rock",
                "Jazz---Latin Jazz",
                "Jazz---Modal",
                "Jazz---Post Bop",
                "Jazz---Ragtime",
                "Jazz---Smooth Jazz",
                "Jazz---Soul-Jazz",
                "Jazz---Space-Age",
                "Jazz---Swing",
                "Latin---Afro-Cuban",
                "Latin---Bai\u00e3o",
                "Latin---Batucada",
                "Latin---Beguine",
                "Latin---Bolero",
                "Latin---Boogaloo",
                "Latin---Bossanova",
                "Latin---Cha-Cha",
                "Latin---Charanga",
                "Latin---Compas",
                "Latin---Cubano",
                "Latin---Cumbia",
                "Latin---Descarga",
                "Latin---Forr\u00f3",
                "Latin---Guaguanc\u00f3",
                "Latin---Guajira",
                "Latin---Guaracha",
                "Latin---MPB",
                "Latin---Mambo",
                "Latin---Mariachi",
                "Latin---Merengue",
                "Latin---Norte\u00f1o",
                "Latin---Nueva Cancion",
                "Latin---Pachanga",
                "Latin---Porro",
                "Latin---Ranchera",
                "Latin---Reggaeton",
                "Latin---Rumba",
                "Latin---Salsa",
                "Latin---Samba",
                "Latin---Son",
                "Latin---Son Montuno",
                "Latin---Tango",
                "Latin---Tejano",
                "Latin---Vallenato",
                "Non-Music---Audiobook",
                "Non-Music---Comedy",
                "Non-Music---Dialogue",
                "Non-Music---Education",
                "Non-Music---Field Recording",
                "Non-Music---Interview",
                "Non-Music---Monolog",
                "Non-Music---Poetry",
                "Non-Music---Political",
                "Non-Music---Promotional",
                "Non-Music---Radioplay",
                "Non-Music---Religious",
                "Non-Music---Spoken Word",
                "Pop---Ballad",
                "Pop---Bollywood",
                "Pop---Bubblegum",
                "Pop---Chanson",
                "Pop---City Pop",
                "Pop---Europop",
                "Pop---Indie Pop",
                "Pop---J-pop",
                "Pop---K-pop",
                "Pop---Kay\u014dkyoku",
                "Pop---Light Music",
                "Pop---Music Hall",
                "Pop---Novelty",
                "Pop---Parody",
                "Pop---Schlager",
                "Pop---Vocal",
                "Reggae---Calypso",
                "Reggae---Dancehall",
                "Reggae---Dub",
                "Reggae---Lovers Rock",
                "Reggae---Ragga",
                "Reggae---Reggae",
                "Reggae---Reggae-Pop",
                "Reggae---Rocksteady",
                "Reggae---Roots Reggae",
                "Reggae---Ska",
                "Reggae---Soca",
                "Rock---AOR",
                "Rock---Acid Rock",
                "Rock---Acoustic",
                "Rock---Alternative Rock",
                "Rock---Arena Rock",
                "Rock---Art Rock",
                "Rock---Atmospheric Black Metal",
                "Rock---Avantgarde",
                "Rock---Beat",
                "Rock---Black Metal",
                "Rock---Blues Rock",
                "Rock---Brit Pop",
                "Rock---Classic Rock",
                "Rock---Coldwave",
                "Rock---Country Rock",
                "Rock---Crust",
                "Rock---Death Metal",
                "Rock---Deathcore",
                "Rock---Deathrock",
                "Rock---Depressive Black Metal",
                "Rock---Doo Wop",
                "Rock---Doom Metal",
                "Rock---Dream Pop",
                "Rock---Emo",
                "Rock---Ethereal",
                "Rock---Experimental",
                "Rock---Folk Metal",
                "Rock---Folk Rock",
                "Rock---Funeral Doom Metal",
                "Rock---Funk Metal",
                "Rock---Garage Rock",
                "Rock---Glam",
                "Rock---Goregrind",
                "Rock---Goth Rock",
                "Rock---Gothic Metal",
                "Rock---Grindcore",
                "Rock---Grunge",
                "Rock---Hard Rock",
                "Rock---Hardcore",
                "Rock---Heavy Metal",
                "Rock---Indie Rock",
                "Rock---Industrial",
                "Rock---Krautrock",
                "Rock---Lo-Fi",
                "Rock---Lounge",
                "Rock---Math Rock",
                "Rock---Melodic Death Metal",
                "Rock---Melodic Hardcore",
                "Rock---Metalcore",
                "Rock---Mod",
                "Rock---Neofolk",
                "Rock---New Wave",
                "Rock---No Wave",
                "Rock---Noise",
                "Rock---Noisecore",
                "Rock---Nu Metal",
                "Rock---Oi",
                "Rock---Parody",
                "Rock---Pop Punk",
                "Rock---Pop Rock",
                "Rock---Pornogrind",
                "Rock---Post Rock",
                "Rock---Post-Hardcore",
                "Rock---Post-Metal",
                "Rock---Post-Punk",
                "Rock---Power Metal",
                "Rock---Power Pop",
                "Rock---Power Violence",
                "Rock---Prog Rock",
                "Rock---Progressive Metal",
                "Rock---Psychedelic Rock",
                "Rock---Psychobilly",
                "Rock---Pub Rock",
                "Rock---Punk",
                "Rock---Rock & Roll",
                "Rock---Rockabilly",
                "Rock---Shoegaze",
                "Rock---Ska",
                "Rock---Sludge Metal",
                "Rock---Soft Rock",
                "Rock---Southern Rock",
                "Rock---Space Rock",
                "Rock---Speed Metal",
                "Rock---Stoner Rock",
                "Rock---Surf",
                "Rock---Symphonic Rock",
                "Rock---Technical Death Metal",
                "Rock---Thrash",
                "Rock---Twist",
                "Rock---Viking Metal",
                "Rock---Y\u00e9-Y\u00e9",
                "Stage & Screen---Musical",
                "Stage & Screen---Score",
                "Stage & Screen---Soundtrack",
                "Stage & Screen---Theme"
            ]

        print("here")
        audio = MonoLoader(filename=file_directory, sampleRate=16000, resampleQuality=4)()
        embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="Embedding_Models/discogs-effnet-bs64-1.pb", output="PartitionedCall:1")
        embeddings = embedding_model(audio)

        # ----------------------- Genre Prediction -----------------------

        model = TensorflowPredict2D(graphFilename="Prediction_Models/Genre_Predictor.pb", input="serving_default_model_Placeholder", output="PartitionedCall:0")
        predictions = model(embeddings)


        # Suppose `predictions` is your (407, 400) array
        predictions = np.array(predictions)

        # Mean pool over the time dimension (axis 0)
        mean_prediction = predictions.mean(axis=0)  # Now shape is (400,)

        # Now find the most probable genre
        predicted_index = np.argmax(mean_prediction)
        predicted_label = labels[predicted_index]
        track_features.append(predicted_label)
        print(f"Predicted Genre: {predicted_label}")


        # ----------------------- Approachability Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Approachability_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        approachability = mean_prediction[1]
        track_features.append(approachability)

        print(f"Predicted Approachability: {mean_prediction}") # Index 0: Negative, Index 1: Positive

        # ----------------------- Engagement Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Engagement_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        engagement = mean_prediction[1]
        track_features.append(engagement)

        print(f"Predicted Engagement: {mean_prediction}") # Index 0: Negative, Index 1: Positive

        # ----------------------- Danceability Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Danceability_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        danceability = mean_prediction[0]
        track_features.append(danceability)

        print(f"Predicted Danceability: {mean_prediction}") # Index 0: Positive, Index 1: Negative


        # ----------------------- Aggressiveness Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Aggressiveness_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        aggressiveness = mean_prediction[0]
        track_features.append(aggressiveness)

        print(f"Predicted Aggressiveness: {mean_prediction}") # Index 0: Positive, Index 1: Negative


        # ----------------------- Happiness Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Mood_Happy_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        happy = mean_prediction[0]
        track_features.append(happy)

        print(f"Predicted Happiness: {mean_prediction}") # Index 0: Positive, Index 1: Negative


        # ----------------------- Party Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Mood_Party_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        party = mean_prediction[1]
        track_features.append(party)

        print(f"Predicted Party: {mean_prediction}") # Index 0: Negative, Index 1: Positive


        # ----------------------- Relaxed Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Mood_Relaxed_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        relaxed = mean_prediction[1]
        track_features.append(relaxed)

        print(f"Predicted Relaxed: {mean_prediction}") # Index 0: Negative, Index 1: Positive


        # ----------------------- Sad Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Mood_Sad_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        sad = mean_prediction[1]
        track_features.append(sad)

        print(f"Predicted Sad: {mean_prediction}") # Index 0: Negative, Index 1: Positive

        # ----------------------- Electronic Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Mood_Electronic_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        electronic = mean_prediction[0]
        track_features.append(electronic)

        print(f"Predicted Electronic: {mean_prediction}") # Index 0: Positive, Index 1: Negative


        # ----------------------- Acoustic Prediction -----------------------
        model = TensorflowPredict2D(graphFilename="Prediction_Models/Mood_Acoustic_Predictor.pb", output="model/Softmax")
        predictions = model(embeddings)
        mean_prediction = predictions.mean(axis=0)
        acoustic = mean_prediction[0]
        track_features.append(acoustic)

        print(f"Predicted Acoustic: {mean_prediction}") # Index 0: Positive, Index 1: Negative

        return track_features
    
    except:
        return -1