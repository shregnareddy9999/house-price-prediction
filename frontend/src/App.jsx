import { useState } from "react";
import "./App.css";

const initialForm = {
  Median_Income: "",
  Median_Age: "",
  Tot_Rooms: "",
  Tot_Bedrooms: "",
  Population: "",
  Households: "",
  Latitude: "",
  Longitude: "",
  Distance_to_coast: "",
  Distance_to_LA: "",
  Distance_to_SanDiego: "",
  Distance_to_SanJose: "",
  Distance_to_SanFrancisco: "",
};

const fields = [
  {
    name: "Median_Income",
    label: "Median income",
    placeholder: "e.g. 5.0",
    unit: "units",
    group: "Property",
    help: "Median household income in the area, measured in $10,000 units.",
  },
  {
    name: "Median_Age",
    label: "Median house age",
    placeholder: "e.g. 30",
    unit: "years",
    group: "Property",
    help: "Median age of houses in the housing block.",
  },
  {
    name: "Tot_Rooms",
    label: "Total rooms",
    placeholder: "e.g. 2000",
    unit: "rooms",
    group: "Property",
    help: "Total number of rooms across the housing block.",
  },
  {
    name: "Tot_Bedrooms",
    label: "Total bedrooms",
    placeholder: "e.g. 400",
    unit: "rooms",
    group: "Property",
    help: "Total number of bedrooms across the housing block.",
  },
  {
    name: "Population",
    label: "Population",
    placeholder: "e.g. 1000",
    unit: "people",
    group: "Property",
    help: "Total population represented by the housing block.",
  },
  {
    name: "Households",
    label: "Households",
    placeholder: "e.g. 350",
    unit: "homes",
    group: "Property",
    help: "Number of households represented by the housing block.",
  },
  {
    name: "Latitude",
    label: "Latitude",
    placeholder: "e.g. 34.0",
    unit: "",
    group: "Location",
    help: "Geographic latitude of the property area, from -90 to 90.",
  },
  {
    name: "Longitude",
    label: "Longitude",
    placeholder: "e.g. -118.0",
    unit: "",
    group: "Location",
    help: "Geographic longitude of the property area, from -180 to 180.",
  },
  {
    name: "Distance_to_coast",
    label: "Distance to coast",
    placeholder: "e.g. 10",
    unit: "km",
    group: "Location",
    help: "Approximate distance from the property area to the coast.",
  },
  {
    name: "Distance_to_LA",
    label: "Distance to Los Angeles",
    placeholder: "e.g. 20",
    unit: "km",
    group: "Location",
    help: "Approximate distance from the property area to Los Angeles.",
  },
  {
    name: "Distance_to_SanDiego",
    label: "Distance to San Diego",
    placeholder: "e.g. 150",
    unit: "km",
    group: "Location",
    help: "Approximate distance from the property area to San Diego.",
  },
  {
    name: "Distance_to_SanJose",
    label: "Distance to San Jose",
    placeholder: "e.g. 500",
    unit: "km",
    group: "Location",
    help: "Approximate distance from the property area to San Jose.",
  },
  {
    name: "Distance_to_SanFrancisco",
    label: "Distance to San Francisco",
    placeholder: "e.g. 550",
    unit: "km",
    group: "Location",
    help: "Approximate distance from the property area to San Francisco.",
  },
];

const validateForm = (formData) => {
  const errors = {};

  const numericFields = [
    "Median_Income",
    "Median_Age",
    "Tot_Rooms",
    "Tot_Bedrooms",
    "Population",
    "Households",
    "Latitude",
    "Longitude",
    "Distance_to_coast",
    "Distance_to_LA",
    "Distance_to_SanDiego",
    "Distance_to_SanJose",
    "Distance_to_SanFrancisco",
  ];

  for (const fieldName of numericFields) {
    const value = formData[fieldName];

    if (value === "" || value === null || value === undefined) {
      errors[fieldName] = "This field is required.";
      continue;
    }

    if (!Number.isFinite(Number(value))) {
      errors[fieldName] = "Please enter a valid number.";
    }
  }

  if (Object.keys(errors).length > 0) {
    return errors;
  }

  const medianIncome = Number(formData.Median_Income);
  const medianAge = Number(formData.Median_Age);
  const totalRooms = Number(formData.Tot_Rooms);
  const totalBedrooms = Number(formData.Tot_Bedrooms);
  const population = Number(formData.Population);
  const households = Number(formData.Households);
  const latitude = Number(formData.Latitude);
  const longitude = Number(formData.Longitude);

  const distanceFields = [
    "Distance_to_coast",
    "Distance_to_LA",
    "Distance_to_SanDiego",
    "Distance_to_SanJose",
    "Distance_to_SanFrancisco",
  ];

  if (medianIncome <= 0) {
    errors.Median_Income = "Median income must be greater than 0.";
  }

  if (medianAge < 0 || medianAge > 200) {
    errors.Median_Age = "Please enter a valid house age.";
  }

  if (totalRooms <= 0) {
    errors.Tot_Rooms = "Total rooms must be greater than 0.";
  }

  if (totalBedrooms <= 0) {
    errors.Tot_Bedrooms = "Total bedrooms must be greater than 0.";
  }

  if (totalBedrooms > totalRooms) {
    errors.Tot_Bedrooms =
      "Total bedrooms cannot be greater than total rooms.";
  }

  if (population <= 0) {
    errors.Population = "Population must be greater than 0.";
  }

  if (households <= 0) {
    errors.Households = "Households must be greater than 0.";
  }

  if (households > population) {
    errors.Households =
      "Households cannot be greater than the population.";
  }

  if (latitude < -90 || latitude > 90) {
    errors.Latitude = "Latitude must be between -90 and 90.";
  }

  if (longitude < -180 || longitude > 180) {
    errors.Longitude = "Longitude must be between -180 and 180.";
  }

  for (const fieldName of distanceFields) {
    if (Number(formData[fieldName]) < 0) {
      errors[fieldName] = "Distance cannot be negative.";
    }
  }

  return errors;
};

function App() {
  const [formData, setFormData] = useState(initialForm);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    if (fieldErrors[name]) {
      setFieldErrors((previous) => ({
        ...previous,
        [name]: "",
      }));
    }

    if (error) {
      setError("");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setPrediction(null);
    setError("");

    const validationErrors = validateForm(formData);

    if (Object.keys(validationErrors).length > 0) {
      setFieldErrors(validationErrors);
      setError("Please review the highlighted fields before continuing.");

      const firstInvalidField = Object.keys(validationErrors)[0];
      const invalidElement = document.getElementById(firstInvalidField);

      if (invalidElement) {
        invalidElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });

        window.setTimeout(() => {
          invalidElement.focus();
        }, 250);
      }

      return;
    }

    setFieldErrors({});
    setLoading(true);

    try {
      const numericData = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [
          key,
          Number(value),
        ])
      );

      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(numericData),
      });

      if (!response.ok) {
        throw new Error("Unable to generate the property valuation.");
      }

      const result = await response.json();

      setPrediction(result.predicted_house_value);
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to connect to the valuation service."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData(initialForm);
    setPrediction(null);
    setError("");
    setFieldErrors({});
  };

  const formatPrice = (value) =>
    value.toLocaleString("en-US", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });

  const renderField = (field) => (
    <div
      className={`field ${fieldErrors[field.name] ? "field-error" : ""}`}
      key={field.name}
    >
      <label htmlFor={field.name}>{field.label}</label>

      <div className="field-input">
        <input
          id={field.name}
          name={field.name}
          type="number"
          step="any"
          value={formData[field.name]}
          placeholder={field.placeholder}
          onChange={handleChange}
          required
          aria-invalid={Boolean(fieldErrors[field.name])}
          aria-describedby={
            fieldErrors[field.name]
              ? `${field.name}-help ${field.name}-error`
              : `${field.name}-help`
          }
          aria-errormessage={
            fieldErrors[field.name] ? `${field.name}-error` : undefined
          }
        />

        {field.unit && <span>{field.unit}</span>}
      </div>

      <p className="field-help" id={`${field.name}-help`}>
        {field.help}
      </p>

      {fieldErrors[field.name] && (
        <p
          className="field-error-message"
          id={`${field.name}-error`}
          role="alert"
        >
          {fieldErrors[field.name]}
        </p>
      )}
    </div>
  );

  return (
    <div className="app">
      <header className="site-header">
        <div className="header-inner">
          <a className="logo" href="/">
            <span className="logo-mark">H</span>
            <span className="logo-name">
              House<span>Value</span>
            </span>
          </a>

          <nav className="navigation">
            <a href="#valuation">Valuation</a>
            <a href="#methodology">Methodology</a>
            <a href="#about">About</a>
          </nav>

          <div className="header-status">
            <span className="status-indicator"></span>
            Model active
          </div>
        </div>
      </header>

      <main>
        <section className="hero" id="valuation">
          <div className="hero-inner">
            <div className="hero-copy">
              <p className="section-label">CALIFORNIA PROPERTY VALUATION</p>

              <h1>
                Know the value
                <br />
                behind the <em>address.</em>
              </h1>

              <p className="hero-text">
                Estimate a property's historical median value using
                location, household and property characteristics through
                a trained machine learning model.
              </p>

              <div className="hero-meta">
                <div>
                  <strong>20,640</strong>
                  <span>properties analyzed</span>
                </div>

                <div className="meta-divider"></div>

                <div>
                  <strong>13</strong>
                  <span>valuation factors</span>
                </div>

                <div className="meta-divider"></div>

                <div>
                  <strong>0.825</strong>
                  <span>R² performance</span>
                </div>
              </div>
            </div>

            <div className="hero-image">
              <div className="image-overlay"></div>

              <div className="image-caption">
                <span>CALIFORNIA</span>
                <span>PROPERTY ANALYTICS</span>
              </div>

              <div className="image-number">01</div>
            </div>
          </div>
        </section>

        <section className="valuation-section">
          <div className="section-heading">
            <div>
              <p className="section-label">PROPERTY PROFILE</p>
              <h2>Build your valuation</h2>
            </div>

            <p className="section-description">
              Enter the characteristics of the property or housing area.
              Helpful examples are shown inside each field.
            </p>
          </div>

          <div className="valuation-layout">
            <div className="form-panel">
              <form onSubmit={handleSubmit} noValidate>
                <div className="form-section">
                  <div className="form-section-heading">
                    <span className="form-index">01</span>

                    <div>
                      <h3>Property characteristics</h3>
                      <p>
                        Basic information about the housing block.
                      </p>
                    </div>
                  </div>

                  <div className="input-grid">
                    {fields
                      .filter((field) => field.group === "Property")
                      .map(renderField)}
                  </div>
                </div>

                <div className="form-section location-section">
                  <div className="form-section-heading">
                    <span className="form-index">02</span>

                    <div>
                      <h3>Location characteristics</h3>

                      <p>
                        Geographic position and distance from major
                        California locations.
                      </p>
                    </div>
                  </div>

                  <div className="input-grid">
                    {fields
                      .filter((field) => field.group === "Location")
                      .map(renderField)}
                  </div>
                </div>

                {error && (
                  <div className="form-error-box" role="alert">
                    <strong>Check your information</strong>
                    <span>{error}</span>
                  </div>
                )}

                <div className="form-footer">
                  <button
                    type="button"
                    className="reset-button"
                    onClick={resetForm}
                    disabled={loading}
                  >
                    Reset values
                  </button>

                  <button
                    type="submit"
                    className="submit-button"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="button-loader"></span>
                        Calculating
                      </>
                    ) : (
                      <>
                        Estimate property value
                        <span>↗</span>
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>

            <aside className="result-panel">
              <div className="result-header">
                <span className="section-label">VALUATION RESULT</span>

                <span className="result-status">
                  <span></span>
                  LIVE
                </span>
              </div>

              <div className="result-main">
                {prediction !== null ? (
                  <>
                    <p>Estimated median value</p>

                    <div className="price">
                      <span>$</span>
                      {formatPrice(prediction)}
                    </div>

                    <div className="result-message">
                      <span className="checkmark">✓</span>
                      Valuation completed successfully
                    </div>
                  </>
                ) : (
                  <>
                    <p>Estimated median value</p>

                    <div className="price empty">
                      <span>$</span>—
                    </div>

                    <p className="result-placeholder">
                      Complete the property profile to generate an
                      estimated value.
                    </p>
                  </>
                )}
              </div>

              {error && (
                <div className="error-box">
                  <strong>Unable to calculate</strong>
                  <span>{error}</span>
                </div>
              )}

              <div className="result-details">
                <div>
                  <span>Model</span>
                  <strong>Random Forest</strong>
                </div>

                <div>
                  <span>Estimators</span>
                  <strong>200 trees</strong>
                </div>

                <div>
                  <span>R² score</span>
                  <strong>0.8250</strong>
                </div>

                <div>
                  <span>Prediction error</span>
                  <strong>$30,407 MAE</strong>
                </div>
              </div>

              <div className="result-note">
                <span>i</span>

                <p>
                  This model is trained on historical California housing
                  data from the 1990 census and should not be interpreted
                  as a current market appraisal.
                </p>
              </div>
            </aside>
          </div>
        </section>

        <section className="methodology" id="methodology">
          <div className="methodology-heading">
            <p className="section-label">HOW IT WORKS</p>

            <h2>
              From property data
              <br />
              to <em>valuation.</em>
            </h2>
          </div>

          <div className="methodology-grid">
            <article>
              <span>01</span>
              <h3>Property data</h3>

              <p>
                Thirteen property and geographic characteristics describe
                the housing block and its surrounding location.
              </p>
            </article>

            <article>
              <span>02</span>
              <h3>Random Forest</h3>

              <p>
                An ensemble of 200 decision trees learns nonlinear
                relationships between the input characteristics and
                historical house values.
              </p>
            </article>

            <article>
              <span>03</span>
              <h3>Estimated value</h3>

              <p>
                The trained model combines the predictions of its trees
                to produce the final estimated median house value.
              </p>
            </article>
          </div>
        </section>

        <section className="performance" id="about">
          <div className="performance-left">
            <p className="section-label">MODEL PERFORMANCE</p>

            <h2>
              Built to explain
              <br />
              the <em>number.</em>
            </h2>

            <p>
              The selected Random Forest model was evaluated on a held-out
              test set. Its performance is reported using standard
              regression metrics rather than relying only on individual
              predictions.
            </p>
          </div>

          <div className="performance-table">
            <div className="performance-row performance-head">
              <span>Metric</span>
              <span>Random Forest</span>
            </div>

            <div className="performance-row">
              <span>R²</span>
              <strong>0.8250</strong>
            </div>

            <div className="performance-row">
              <span>MAE</span>
              <strong>$30,407.79</strong>
            </div>

            <div className="performance-row">
              <span>RMSE</span>
              <strong>$47,883.47</strong>
            </div>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div>
          <strong>HouseValue</strong>
          <span>California property analytics</span>
        </div>

        <div>
          <span>Random Forest Regression</span>
          <span>·</span>
          <span>Local inference</span>
        </div>
      </footer>
    </div>
  );
}

export default App;