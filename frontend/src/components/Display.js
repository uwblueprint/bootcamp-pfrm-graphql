import React from 'react';
import { useQuery, gql } from '@apollo/client';

import BasicTable from './BasicTable';
import './Display.scss';
import  { removeTypeName } from '../utilities';

const restaurantsQuery = gql`
  {
    getAllRestaurants {
      id
      name
      address
      type
      budget
      description
      rating
    }
  }
`;

const Display = (props) => {
  /**
   * useQuery is a React Hook (refer to accompanying slides for a quick explanation).
   * when this component renders, it executes the provided GraphQL query using our
   * Apollo client, obtaining the data we need
   */
  const { loading, error, data } = useQuery(restaurantsQuery, {
    onCompleted: data => { props.loadData(removeTypeName(data.getAllRestaurants)) }
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error loading restaurants!</p>;

  return (
    <div className="display-container">
      <h2>Local Data Handling</h2>
      <BasicTable data={removeTypeName(data.getAllRestaurants)} />
      <h2>Global Data Handling</h2>
      <BasicTable  data={props.storeData} />
    </div>
  );
}

export default Display;

Display.propTypes = {};
