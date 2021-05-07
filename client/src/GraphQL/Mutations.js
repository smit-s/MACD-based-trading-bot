import { gql } from "@apollo/client";

export const CREATE_USER_MUTATION = gql`
  mutation createUser(
    $email: String!
    $password: String!
    $dateOfBirth: String!
    $encryptedUserId: String
    $encryptedPassword: String
    $key: String
    $shortWindow: String
    $longWindow: String
    $signal: String
    $series_len: String
    $macdLimit: String
    $scripCode: String
    $scripNum: String
    $tradeQty: String
    $gap: String
    $tickTime: String


  ) {
    createUser(
    email:  $email
    password:  $password
    dateOfBirth:  $dateOfBirth
    encryptedUserId:  $encryptedUserId
    encryptedPassword:  $encryptedPassword
    key:  $key
    shortWindow: $shortWindow
    longWindow: $longWindow
    signal: $signal
    series_len :$series_len
    macdLimit: $macdLimit
    scripCode: $scripCode
    scripNum: $scripNum
    tradeQty: $tradeQty
    gap: $gap
    tickTime: $tickTime
    ) {
      id
    }
  }
`;
